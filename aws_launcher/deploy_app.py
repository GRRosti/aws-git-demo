import boto3
import time
import paramiko
import uuid
import os
import configparser
import socket
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

# AWS configuration
AWS_REGION = 'us-west-2'
INSTANCE_TYPE = 't3.micro'
GITHUB_GAME_REPO = 'https://github.com/GRRosti/aws-git-demo.git'  # Repository containing pokemon_game
GAME_PORT = 8000  # Port for server-based game (adjust if needed)
USER_DATA_FILE = 'aws_launcher/user_data.sh'
CREDENTIALS_FILE = 'aws_launcher/credentials.txt'

# Generate a unique key pair name
KEY_NAME = f'app-key-{uuid.uuid4().hex[:8]}'

# Load credentials from local credentials file
def load_credentials():
    """Load AWS credentials from local credentials file."""
    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(f"Credentials file not found: {CREDENTIALS_FILE}")
    
    config = configparser.ConfigParser()
    config.read(CREDENTIALS_FILE)
    
    try:
        access_key = config['default']['aws_access_key_id']
        secret_key = config['default']['aws_secret_access_key']
        session_token = config['default'].get('aws_session_token', None)
        
        if not all([access_key, secret_key]):
            raise ValueError("Missing required credentials (aws_access_key_id or aws_secret_access_key)")
        
        return access_key, secret_key, session_token
    except KeyError as e:
        raise ValueError(f"Invalid credentials file format: missing {e}")

# Initialize Boto3 session with local credentials
try:
    access_key, secret_key, session_token = load_credentials()
    session_params = {
        'aws_access_key_id': access_key,
        'aws_secret_access_key': secret_key,
        'region_name': AWS_REGION
    }
    if session_token:
        session_params['aws_session_token'] = session_token
    
    boto3_session = boto3.Session(**session_params)
    ec2_client = boto3_session.client('ec2')
    ec2_resource = boto3_session.resource('ec2')
    
    # Validate credentials
    ec2_client.describe_regions()
except FileNotFoundError as e:
    raise Exception(f"Credentials file error: {e}")
except ValueError as e:
    raise Exception(f"Credentials file error: {e}")
except NoCredentialsError:
    raise Exception("No AWS credentials found in credentials file.")
except PartialCredentialsError:
    raise Exception("Incomplete AWS credentials in credentials file.")
except ClientError as e:
    if e.response['Error']['Code'] == 'RequestExpired':
        raise Exception(
            "AWS credentials have expired. Please refresh them using 'aws sts assume-role' "
            "or 'aws sso login' and update aws_launcher/credentials.txt."
        )
    raise Exception(f"Error initializing AWS session: {e}")

def get_latest_amazon_linux_2_ami():
    """Fetch the latest Amazon Linux 2 AMI ID."""
    try:
        response = ec2_client.describe_images(
            Filters=[
                {'Name': 'name', 'Values': ['amzn2-ami-hvm-*-x86_64-gp2']},
                {'Name': 'state', 'Values': ['available']},
                {'Name': 'architecture', 'Values': ['x86_64']},
                {'Name': 'virtualization-type', 'Values': ['hvm']},
                {'Name': 'owner-alias', 'Values': ['amazon']}
            ],
            Owners=['amazon']
        )
        images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
        if not images:
            raise Exception("No Amazon Linux 2 AMI found")
        return images[0]['ImageId']
    except ClientError as e:
        raise Exception(f"Error fetching AMI: {e}")

def create_key_pair():
    """Create and save an SSH key pair."""
    try:
        key_pair = ec2_client.create_key_pair(KeyName=KEY_NAME)
        with open(f'{KEY_NAME}.pem', 'w') as f:
            os.chmod(f'{KEY_NAME}.pem', 0o400)
            f.write(key_pair['KeyMaterial'])
        return KEY_NAME
    except ClientError as e:
        raise Exception(f"Error creating key pair: {e}")

def create_vpc_and_network():
    """Create VPC, subnet, internet gateway, and route table."""
    try:
        vpc = ec2_resource.create_vpc(CidrBlock='10.0.0.0/16')
        vpc.create_tags(Tags=[{'Key': 'Name', 'Value': 'AppVPC'}])
        vpc.wait_until_available()

        igw = ec2_resource.create_internet_gateway()
        igw.attach_to_vpc(VpcId=vpc.id)
        igw.create_tags(Tags=[{'Key': 'Name', 'Value': 'AppIGW'}])

        subnet = vpc.create_subnet(CidrBlock='10.0.1.0/24')
        subnet.create_tags(Tags=[{'Key': 'Name', 'Value': 'AppSubnet'}])
        
        # Enable auto-assign public IP for the subnet
        ec2_client.modify_subnet_attribute(
            SubnetId=subnet.id,
            MapPublicIpOnLaunch={'Value': True}
        )

        route_table = vpc.create_route_table()
        route_table.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=igw.id)
        route_table.associate_with_subnet(SubnetId=subnet.id)
        route_table.create_tags(Tags=[{'Key': 'Name', 'Value': 'AppRouteTable'}])

        return vpc.id, subnet.id
    except ClientError as e:
        raise Exception(f"Error creating network resources: {e}")

def create_security_group(vpc_id):
    """Create a security group with SSH and game port access."""
    try:
        sg = ec2_resource.create_security_group(
            GroupName=f'app-sg-{uuid.uuid4().hex[:8]}',
            Description='Security group for game server',
            VpcId=vpc_id
        )
        sg.authorize_ingress(
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': GAME_PORT,
                    'ToPort': GAME_PORT,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        )
        sg.create_tags(Tags=[{'Key': 'Name', 'Value': 'GameSG'}])
        return sg.id
    except ClientError as e:
        raise Exception(f"Error creating security group: {e}")

def check_instance_connectivity(ip_address, port=22, timeout=2):
    """Check connectivity to the instance by attempting a TCP connection."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip_address, port))
        sock.close()
        if result == 0:
            print(f"Connectivity to {ip_address}:{port} successful.")
            return True
        else:
            print(f"Connectivity to {ip_address}:{port} failed (error code: {result}).")
            return False
    except Exception as e:
        print(f"Error checking connectivity to {ip_address}:{port}: {e}")
        return False

def check_instance_status(instance_id):
    """Verify the instance is running."""
    try:
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        state = response['Reservations'][0]['Instances'][0]['State']['Name']
        if state != 'running':
            raise Exception(f"Instance {instance_id} is not running. Current state: {state}")
        print(f"Instance {instance_id} is running.")
    except ClientError as e:
        raise Exception(f"Error checking instance status: {e}")

def launch_ec2_instance(subnet_id, sg_id, key_name):
    """Launch EC2 instance with minimal user data."""
    try:
        ami_id = get_latest_amazon_linux_2_ami()
        user_data = """#!/bin/bash
        yum update -y
        """
        instance = ec2_resource.create_instances(
            ImageId=ami_id,
            InstanceType=INSTANCE_TYPE,
            MinCount=1,
            MaxCount=1,
            SubnetId=subnet_id,
            SecurityGroupIds=[sg_id],
            KeyName=key_name,
            UserData=user_data,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': 'GameServer'}]
            }]
        )[0]
        instance.wait_until_running()
        instance.reload()
        if not instance.public_ip_address:
            # Fallback: Associate an Elastic IP
            allocation = ec2_client.allocate_address(Domain='vpc')
            ec2_client.associate_address(
                InstanceId=instance.id,
                AllocationId=allocation['AllocationId']
            )
            instance.reload()
            return instance.id, instance.public_ip_address, allocation['AllocationId']
        return instance.id, instance.public_ip_address, None
    except ClientError as e:
        raise Exception(f"Error launching EC2 instance: {e}")

def setup_and_launch_game(ip_address, key_name):
    """Connect via SSH, clone the game repo, install and compile the game, and set up auto-launch."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        key = paramiko.RSAKey.from_private_key_file(f'{KEY_NAME}.pem')
        print(f"Connecting to {ip_address} via SSH...")
        
        for _ in range(30):
            try:
                ssh.connect(ip_address, username='ec2-user', pkey=key)
                print("SSH connection established.")
                
                commands = [
                    "sudo yum update -y",
                    "sudo yum install -y git python3 python3-pip",
                    "pip3 install pyinstaller pygame",
                    f"git clone {GITHUB_GAME_REPO} /home/ec2-user/game",
                    "ls -lR /home/ec2-user/game",  # Debug: Recursively list all files
                    "[ -d /home/ec2-user/game/pokemon_game ] || echo 'Error: pokemon_game directory not found'",
                    "cd /home/ec2-user/game/pokemon_game",
                    "ls -l",  # Debug: Check pokemon_game contents
                    # Find Python files
                    "find . -maxdepth 1 -type f -name '*.py' || echo 'Error: No Python files found'",
                    # Identify main script
                    "MAIN_PY=$(find . -maxdepth 1 -type f -name '*.py' | head -n 1); [ -n \"$MAIN_PY\" ] && basename \"$MAIN_PY\" || echo 'Error: No main script found'",
                    "[ -f main.py ] || echo 'Trying main.py: Not found'",
                    # Run pyinstaller
                    "[ -f main.py ] && pyinstaller --onefile main.py > pyinstaller.log 2>&1 || echo 'Skipping pyinstaller for main.py'",
                    "[ ! -f main.py ] && [ -n \"$MAIN_PY\" ] && pyinstaller --onefile \"$MAIN_PY\" > pyinstaller.log 2>&1 || echo 'Skipping pyinstaller for alternative script'",
                    # Check executable
                    "[ -f dist/main/main ] || [ -n \"$MAIN_PY\" ] && [ -f dist/$(basename \"$MAIN_PY\" .py)/$(basename \"$MAIN_PY\" .py) ] || echo 'Error: main executable not found'",
                    # Set permissions
                    "[ -f dist/main/main ] && sudo chmod +x dist/main/main || [ -n \"$MAIN_PY\" ] && sudo chmod +x dist/$(basename \"$MAIN_PY\" .py)/$(basename \"$MAIN_PY\" .py) || echo 'Skipping chmod'",
                    # Set up auto-launch with welcome message
                    "echo 'echo \"Welcome to Pokemon Game! Attempting to launch...\"' >> ~/.bashrc",
                    "MAIN_EXEC=$( [ -f dist/main/main ] && echo 'dist/main/main' || echo \"dist/$(basename \"$MAIN_PY\" .py)/$(basename \"$MAIN_PY\" .py)\" ); echo '[ -t 0 ] && [ -f /home/ec2-user/game/pokemon_game/$MAIN_EXEC ] && /home/ec2-user/game/pokemon_game/$MAIN_EXEC || echo \"Error: Game executable not found\"' >> ~/.bashrc",
                    # Verify shell and .bashrc
                    "echo $SHELL",
                    "cat ~/.bashrc",
                    # Test executable
                    "[ -f dist/main/main ] && ./dist/main/main || [ -n \"$MAIN_PY\" ] && ./dist/$(basename \"$MAIN_PY\" .py)/$(basename \"$MAIN_PY\" .py) || echo 'Error: Cannot run main executable'",
                    # Show pyinstaller log if needed
                    "[ ! -f dist/main/main ] && [ ! -f dist/$(basename \"$MAIN_PY\" .py)/$(basename \"$MAIN_PY\" .py) ] && cat pyinstaller.log || echo 'PyInstaller log not needed'"
                ]
                
                for cmd in commands:
                    print(f"Executing: {cmd}")
                    stdin, stdout, stderr = ssh.exec_command(cmd)
                    exit_status = stdout.channel.recv_exit_status()
                    stdout_output = stdout.read().decode()
                    stderr_output = stderr.read().decode()
                    if stdout_output:
                        print(f"Output: {stdout_output}")
                    if stderr_output:
                        print(f"Error output: {stderr_output}")
                    if exit_status != 0 and "ls" not in cmd and "echo" not in cmd and ">>" not in cmd and "find" not in cmd and "cat" not in cmd:
                        print(f"Error executing {cmd}: Exit status {exit_status}")
                        return False
                
                print("Game setup complete. Game should auto-launch on SSH login.")
                return True
            except Exception as e:
                print(f"Waiting for SSH... {e}")
                time.sleep(10)
        return False
    except Exception as e:
        raise Exception(f"Error during SSH setup or game launch: {e}")
    finally:
        ssh.close()

def cleanup_resources(instance_id, vpc_id, sg_id, key_name, allocation_id):
    """Clean up AWS resources."""
    try:
        if instance_id:
            ec2_client.terminate_instances(InstanceIds=[instance_id])
            print(f"Terminated instance: {instance_id}")
        
        if allocation_id:
            ec2_client.release_address(AllocationId=allocation_id)
            print(f"Released Elastic IP: {allocation_id}")
        
        if sg_id:
            ec2_client.delete_security_group(GroupId=sg_id)
            print(f"Deleted security group: {sg_id}")
        
        if vpc_id:
            vpc = ec2_resource.Vpc(vpc_id)
            for subnet in vpc.subnets.all():
                subnet.delete()
                print(f"Deleted subnet: {subnet.id}")
            
            for igw in vpc.internet_gateways.all():
                igw.detach_from_vpc(VpcId=vpc_id)
                igw.delete()
                print(f"Deleted internet gateway: {igw.id}")
            
            for rt in vpc.route_tables.all():
                rt.delete()
                print(f"Deleted route table: {rt.id}")
            
            vpc.delete()
            print(f"Deleted VPC: {vpc_id}")
        
        if key_name:
            ec2_client.delete_key_pair(KeyName=key_name)
            if os.path.exists(f'{key_name}.pem'):
                os.remove(f'{key_name}.pem')
            print(f"Deleted key pair: {key_name}")
    except ClientError as e:
        print(f"Error during cleanup: {e}")

def main():
    vpc_id = subnet_id = sg_id = instance_id = public_ip = key_name = allocation_id = None
    try:
        print("Creating infrastructure...")
        key_name = create_key_pair()
        vpc_id, subnet_id = create_vpc_and_network()
        sg_id = create_security_group(vpc_id)
        instance_id, public_ip, allocation_id = launch_ec2_instance(subnet_id, sg_id, key_name)
        
        print(f"Instance launched: {instance_id}")
        print(f"Public IP: {public_ip}")
        print(f"SSH Key saved as: {key_name}.pem")
        
        check_instance_status(instance_id)
        
        if not check_instance_connectivity(public_ip):
            raise Exception(f"Instance {public_ip} is not reachable.")
        
        if setup_and_launch_game(public_ip, key_name):
            print(f"Game setup complete! SSH into instance to play: ssh -i {key_name}.pem ec2-user@{public_ip}")
            print(f"If the game is server-based, access it at http://{public_ip}:{GAME_PORT}")
        else:
            print("Failed to set up or launch the game.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if instance_id or vpc_id or sg_id or key_name or allocation_id:
            cleanup = input("Do you want to clean up AWS resources? (y/n): ").lower() == 'y'
            if cleanup:
                print("Cleaning up resources...")
                cleanup_resources(instance_id, vpc_id, sg_id, key_name, allocation_id)

if __name__ == "__main__":
    main()