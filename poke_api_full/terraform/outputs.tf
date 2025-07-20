# terraform/outputs.tf

output "backend_ec2_public_ip" {
  description = "The public IP address of the Backend EC2 instance."
  value       = aws_instance.backend_ec2.public_ip
}

output "game_ec2_public_ip" {
  description = "The public IP address of the Game EC2 instance."
  value       = aws_instance.game_ec2.public_ip
}

output "backend_ec2_private_ip" {
  description = "The private IP address of the Backend EC2 instance."
  value       = aws_instance.backend_ec2.private_ip
}

output "game_ec2_private_ip" {
  description = "The private IP address of the Game EC2 instance."
  value       = aws_instance.game_ec2.private_ip
}

output "dynamodb_table_name" {
  description = "The name of the DynamoDB table created."
  value       = aws_dynamodb_table.game_data_table.name
}

output "backend_ssh_command" {
  description = "SSH command to connect to the Backend EC2 instance (replace .pem with your key file)."
  value       = "ssh -i ~/.ssh/${var.key_pair_name}.pem ec2-user@${aws_instance.backend_ec2.public_ip}"
  sensitive   = true
}

output "game_ssh_command" {
  description = "SSH command to connect to the Game EC2 instance (replace .pem with your key file)."
  value       = "ssh -i ~/.ssh/${var.key_pair_name}.pem ec2-user@${aws_instance.game_ec2.public_ip}"
  sensitive   = true
}
