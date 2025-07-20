# terraform/variables.tf

variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-west-2"
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instance. Use an Amazon Linux 2 AMI for yum commands."
  type        = string
  default     = "ami-088b43f1b52d7ca18" # <<< REPLACE WITH A VALID AMI ID FOR YOUR REGION >>>
}

variable "instance_type" {
  description = "The EC2 instance type (e.g., t2.micro, t3.small)."
  type        = string
  default     = "t3.micro"
}

variable "key_pair_name" {
  description = "The name of an existing EC2 Key Pair to allow SSH access to the instances."
  type        = string
  # IMPORTANT: You must create this key pair in the AWS EC2 console or via Terraform beforehand.
  # default     = "my-ssh-key" # <<< UNCOMMENT AND REPLACE WITH YOUR KEY PAIR NAME >>>
}

variable "github_repo_url" {
  description = "The URL of the GitHub repository containing all project code (Terraform, Ansible, Apps)."
  type        = string
  # IMPORTANT: Replace this with the actual URL of your GitHub repository.
  # Ensure it's a public repository or configure SSH keys/PAT for private access.
  default     = "https://github.com/your-username/distributed-pokeapp.git" # <<< REPLACE THIS >>>
}

variable "dynamodb_table_name" {
  description = "The name for the DynamoDB table (if used by game/backend directly)."
  type        = string
  default     = "PokeGameData"
}

variable "iam_instance_profile_name" {
  description = "The name for the IAM instance profile for EC2 (for DynamoDB access)."
  type        = string
  default     = "DistributedAppEC2Profile"
}
