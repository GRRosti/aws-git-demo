# terraform/main.tf

# AWS Provider Configuration
provider "aws" {
  region = var.aws_region
}

# -----------------------------------------------------------------------------
# VPC Network Setup
# -----------------------------------------------------------------------------

# Create a new VPC for the distributed application
resource "aws_vpc" "app_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "DistributedAppVPC"
  }
}

# Create a public subnet within the VPC
resource "aws_subnet" "app_subnet" {
  vpc_id            = aws_vpc.app_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.aws_region}a"
  map_public_ip_on_launch = true # Instances in this subnet get a public IP
  tags = {
    Name = "DistributedAppSubnet"
  }
}

# Create an Internet Gateway
resource "aws_internet_gateway" "app_igw" {
  vpc_id = aws_vpc.app_vpc.id
  tags = {
    Name = "DistributedAppIGW"
  }
}

# Create a Route Table for the public subnet
resource "aws_route_table" "app_route_table" {
  vpc_id = aws_vpc.app_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.app_igw.id
  }
  tags = {
    Name = "DistributedAppRouteTable"
  }
}

# Associate the Route Table with the public subnet
resource "aws_route_table_association" "app_rta" {
  subnet_id      = aws_subnet.app_subnet.id
  route_table_id = aws_route_table.app_route_table.id
}

# -----------------------------------------------------------------------------
# Security Groups
# -----------------------------------------------------------------------------

# Security Group for Backend EC2 Instance (EC2 Instance 1)
resource "aws_security_group" "backend_sg" {
  vpc_id      = aws_vpc.app_vpc.id
  name        = "backend-ec2-sg"
  description = "Security group for backend EC2 instance"

  # Allow SSH from anywhere (for Ansible control machine or manual access)
  # IMPORTANT: Restrict to your specific IP range in production!
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow SSH"
  }

  # Allow Flask API traffic (e.g., port 5000) from the Game EC2 instance's security group
  ingress {
    from_port   = 5000 # Flask API port
    to_port     = 5000
    protocol    = "tcp"
    security_groups = [aws_security_group.game_sg.id] # Only from Game EC2
    description = "Allow Flask API from Game EC2"
  }

  # Allow MongoDB traffic (port 27017) from the Backend EC2 itself (Docker containers)
  ingress {
    from_port   = 27017 # MongoDB default port
    to_port     = 27017
    protocol    = "tcp"
    self        = true # Allow from within this security group (for Docker internal comms)
    description = "Allow MongoDB from self (Docker)"
  }

  # Allow all outbound traffic (for updates, cloning repos, etc.)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "BackendEC2SecurityGroup"
  }
}

# Security Group for Game EC2 Instance (EC2 Instance 2)
resource "aws_security_group" "game_sg" {
  vpc_id      = aws_vpc.app_vpc.id
  name        = "game-ec2-sg"
  description = "Security group for game EC2 instance"

  # Allow SSH from anywhere (for Ansible control machine or manual access)
  # IMPORTANT: Restrict to your specific IP range in production!
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow SSH"
  }

  # If your game has a web interface, open its port (e.g., 80 or 8000)
  ingress {
    from_port   = 8000 # Example game web interface port
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTP access to game"
  }

  # Allow all outbound traffic (to Backend API, external PokeAPI, etc.)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "GameEC2SecurityGroup"
  }
}

# -----------------------------------------------------------------------------
# EC2 Instances
# -----------------------------------------------------------------------------

# Common user data script for both instances to set up Ansible
# This script will:
# 1. Update system packages.
# 2. Install Git, Python3, and pip.
# 3. Install Ansible.
# 4. Clone the entire project repository from GitHub.
# 5. Execute the specific Ansible playbook for the instance.
locals {
  common_user_data_script = <<-EOF
    #!/bin/bash
    echo "Starting common EC2 user data script..." >> /var/log/user_data.log

    # Update system packages
    sudo yum update -y
    echo "System updated." >> /var/log/user_data.log

    # Install Git, Python3, and pip
    sudo yum install -y git python3 python3-pip
    echo "Git, Python, pip installed." >> /var/log/user_data.log

    # Install Ansible
    pip3 install ansible
    echo "Ansible installed." >> /var/log/user_data.log

    # Define the project directory
    PROJECT_DIR="/home/ec2-user/distributed-pokeapp"

    # Clone the entire project repository from GitHub
    # IMPORTANT: Replace '${var.github_repo_url}' with the actual URL of your GitHub repository
    # containing all Terraform, Ansible, and application code.
    echo "Cloning project repository from ${var.github_repo_url}..." >> /var/log/user_data.log
    git clone ${var.github_repo_url} ${PROJECT_DIR}
    if [ $? -ne 0 ]; then
        echo "Error: Failed to clone project repository." >> /var/log/user_data.log
        exit 1
    fi
    echo "Project repository cloned to ${PROJECT_DIR}." >> /var/log/user_data.log

    # Change ownership to ec2-user
    sudo chown -R ec2-user:ec2-user ${PROJECT_DIR}
    echo "Changed ownership of project directory." >> /var/log/user_data.log

    # Navigate to the Ansible directory within the cloned repo
    cd ${PROJECT_DIR}/ansible
    echo "Changed directory to ${PWD}" >> /var/log/user_data.log

    # Generate Ansible inventory from template
    # This will be done dynamically by Terraform and passed via user_data
    # For self-provisioning, we'll generate it on the fly or use localhost.
    # A better approach for multi-node is to run Ansible from a control machine.
    # For this exercise, we'll demonstrate a simplified self-provisioning.
    # The actual inventory will be created by Terraform's templatefile function.
    # The playbook will be run with `--connection=local` or target localhost.
    EOF
}

# Backend EC2 Instance (EC2 Instance 1)
resource "aws_instance" "backend_ec2" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.app_subnet.id
  associate_public_ip_address = true
  vpc_security_group_ids = [aws_security_group.backend_sg.id]
  key_name               = var.key_pair_name
  iam_instance_profile   = var.iam_instance_profile_name # For DynamoDB access if backend uses it directly

  # User data script to install Ansible and run backend playbook
  user_data = <<-EOF
    ${local.common_user_data_script}

    # Generate Ansible inventory for localhost
    echo "[backend_servers]" > inventory.ini
    echo "localhost ansible_connection=local ansible_user=ec2-user" >> inventory.ini
    echo "Generated inventory.ini for backend." >> /var/log/user_data.log

    # Run the backend Ansible playbook
    echo "Running backend Ansible playbook..." >> /var/log/user_data.log
    ansible-playbook -i inventory.ini backend.yml >> /var/log/user_data.log 2>&1 &
    echo "Backend Ansible playbook launched." >> /var/log/user_data.log
    EOF

  tags = {
    Name = "DistributedAppBackendEC2"
    Role = "Backend"
  }
}

# Game EC2 Instance (EC2 Instance 2)
resource "aws_instance" "game_ec2" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.app_subnet.id
  associate_public_ip_address = true
  vpc_security_group_ids = [aws_security_group.game_sg.id]
  key_name               = var.key_pair_name

  # User data script to install Ansible and run game playbook
  user_data = <<-EOF
    ${local.common_user_data_script}

    # Generate Ansible inventory for localhost
    echo "[game_servers]" > inventory.ini
    echo "localhost ansible_connection=local ansible_user=ec2-user backend_private_ip=${aws_instance.backend_ec2.private_ip}" >> inventory.ini
    echo "Generated inventory.ini for game." >> /var/log/user_data.log

    # Run the game Ansible playbook
    echo "Running game Ansible playbook..." >> /var/log/user_data.log
    ansible-playbook -i inventory.ini game.yml >> /var/log/user_data.log 2>&1 &
    echo "Game Ansible playbook launched." >> /var/log/user_data.log
    EOF

  tags = {
    Name = "DistributedAppGameEC2"
    Role = "Game"
  }
}

# -----------------------------------------------------------------------------
# DynamoDB Table (Optional, if backend needs direct DynamoDB access)
# -----------------------------------------------------------------------------

# Create a DynamoDB table (if the backend or game needs direct access)
# This is separate from the MongoDB used by the Flask API.
# If your Flask API is the only one interacting with DB, and it uses MongoDB,
# then this DynamoDB table might be for a different purpose or can be removed.
# Assuming it's for some game-specific data not handled by the Flask API.
resource "aws_dynamodb_table" "game_data_table" {
  name             = var.dynamodb_table_name
  billing_mode     = "PROVISIONED"
  read_capacity    = 5
  write_capacity   = 5
  hash_key         = "GameId"

  attribute {
    name = "GameId"
    type = "S"
  }

  tags = {
    Name = "GameDataTable"
  }
}

# IAM Role and Instance Profile for EC2 to access DynamoDB
# This is only needed if your EC2 instances directly access DynamoDB,
# not if the Flask API (which uses MongoDB) is the sole backend.
# Assuming the game or another part of the backend might use it.
resource "aws_iam_role" "ec2_dynamodb_role" {
  name = "ec2-dynamodb-access-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy" "ec2_dynamodb_policy" {
  name = "ec2-dynamodb-access-policy"
  role = aws_iam_role.ec2_dynamodb_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:BatchGetItem",
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan",
        ]
        Effect   = "Allow"
        Resource = aws_dynamodb_table.game_data_table.arn
      },
    ]
  })
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = var.iam_instance_profile_name
  role = aws_iam_role.ec2_dynamodb_role.name
}
