import boto3
import time
import paramiko
import uuid
import os
import configparser
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

# AWS configuration
AWS_REGION = 'us-west-2'
INSTANCE_ID = 'i-09f4156b94f9ae64e'  # Specified instance ID
CREDENTIALS_FILE = 'aws_launcher/credentials.txt'

# Generate a unique key pair name (if needed)
KEY_NAME = '/workspaces/aws-git-demo/app-key-b82bc2f6.pem'
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
            "or 'aws sso login' and update the credentials file."
        )
    raise Exception(f"Error initializing AWS session: {e}")

def get_instance_public_ip(instance_id):
    """Check if the instance has a public IP; if not, associate an Elastic IP."""
    try:
        response = ec2_client.describe_instances(
            InstanceIds=[instance_id],
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        )
        instance = response['Reservations'][0]['Instances'][0]
        public_ip = instance.get('PublicIpAddress')
        
        if public_ip:
            print(f"Instance {instance_id} already has public IP: {public_ip}")
            return public_ip, None
        
        # Allocate and associate an Elastic IP
        allocation = ec2_client.allocate_address(Domain='vpc')
        allocation_id = allocation['AllocationId']
        public_ip = allocation['PublicIp']
        ec2_client.associate_address(
            InstanceId=instance_id,
            AllocationId=allocation_id
        )
        print(f"Associated Elastic IP {public_ip} with instance {instance_id}")
        return public_ip, allocation_id
    except ClientError as e:
        raise Exception(f"Error checking/associating public IP: {e}")

def verify_security_group(instance_id):
    """Ensure the instance's security group allows SSH."""
    try:
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        security_group_id = response['Reservations'][0]['Instances'][0]['SecurityGroups'][0]['GroupId']
        
        # Check existing ingress rules
        sg = ec2_client.describe_security_groups(GroupIds=[security_group_id])
        ssh_rule_exists = any(
            perm['IpProtocol'] == 'tcp' and perm['FromPort'] == 22 and perm['ToPort'] == 22
            for perm in sg['SecurityGroups'][0]['IpPermissions']
        )
        
        if not ssh_rule_exists:
            ec2_client.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 22,
                        'ToPort': 22,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    }
                ]
            )
            print(f"Added SSH ingress rule to security group {security_group_id}")
        return security_group_id
    except ClientError as e:
        raise Exception(f"Error verifying security group: {e}")

def verify_instance(ip_address, key_name):
    """Verify instance setup via SSH."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        key = paramiko.RSAKey.from_private_key_file(f'{key_name}.pem')
        for _ in range(30):
            try:
                ssh.connect(ip_address, username='ec2-user', pkey=key)
                stdin, stdout, stderr = ssh.exec_command('cat /etc/motd')
                print("MOTD Content:")
                print(stdout.read().decode())
                return True
            except Exception as e:
                print(f"Waiting for SSH... {e}")
                time.sleep(10)
        return False
    except Exception as e:
        raise Exception(f"Error verifying instance: {e}")
    finally:
        ssh.close()

def cleanup_resources(allocation_id, security_group_id):
    """Clean up Elastic IP and security group rules."""
    try:
        if allocation_id:
            ec2_client.release_address(AllocationId=allocation_id)
            print(f"Released Elastic IP: {allocation_id}")
        
        if security_group_id:
            try:
                ec2_client.revoke_security_group_ingress(
                    GroupId=security_group_id,
                    IpPermissions=[
                        {
                            'IpProtocol': 'tcp',
                            'FromPort': 22,
                            'ToPort': 22,
                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                        }
                    ]
                )
                print(f"Removed SSH ingress rule from security group {security_group_id}")
            except ClientError as e:
                if e.response['Error']['Code'] != 'InvalidPermission.NotFound':
                    raise
    except ClientError as e:
        print(f"Error during cleanup: {e}")

def main():
    allocation_id = security_group_id = public_ip = None
    try:
        print(f"Processing instance {INSTANCE_ID}...")
        public_ip, allocation_id = get_instance_public_ip(INSTANCE_ID)
        security_group_id = verify_security_group(INSTANCE_ID)
        
        print(f"Verifying SSH access to {public_ip}...")
        if verify_instance(public_ip, KEY_NAME):
            print(f"SSH connection successful! Access instance with:")
            print(f"ssh -i {KEY_NAME}.pem ec2-user@{public_ip}")
        else:
            print("Failed to verify SSH connection.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if allocation_id or security_group_id:
            cleanup = input("Do you want to clean up Elastic IP and security group rules? (y/n): ").lower() == 'y'
            if cleanup:
                print("Cleaning up resources...")
                cleanup_resources(allocation_id, security_group_id)

if __name__ == "__main__":
    main()