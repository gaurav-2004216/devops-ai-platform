output "vpc_id" {
  description = "DevSecOps VPC ID"
  value       = aws_vpc.devops.id
}

output "public_subnet_id" {
  description = "DevSecOps public subnet ID"
  value       = aws_subnet.public.id
}

output "availability_zone" {
  description = "Availability zone"
  value       = aws_subnet.public.availability_zone
}

output "security_group_id" {
  description = "DevSecOps security group ID"
  value       = aws_security_group.devops.id
}
output "instance_id" {
  description = "Terraform DevOps EC2 instance ID"
  value       = aws_instance.devops.id
}

output "instance_public_ip" {
  description = "Terraform DevOps EC2 public IP"
  value       = aws_instance.devops.public_ip
}
output "ebs_volume_id" {
  description = "Persistent EBS volume ID"
  value       = aws_ebs_volume.devops_data.id
}

output "ebs_volume_size" {
  description = "Persistent EBS volume size in GB"
  value       = aws_ebs_volume.devops_data.size
}
