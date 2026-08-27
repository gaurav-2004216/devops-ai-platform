resource "aws_vpc" "devops" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name    = "devops-vpc"
    Project = "DevSecOps"
  }
}

resource "aws_internet_gateway" "devops" {
  vpc_id = aws_vpc.devops.id

  tags = {
    Name    = "devops-igw"
    Project = "DevSecOps"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.devops.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "ap-south-1a"
  map_public_ip_on_launch = true

  tags = {
    Name    = "devops-public-subnet"
    Project = "DevSecOps"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.devops.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.devops.id
  }

  tags = {
    Name    = "devops-public-rt"
    Project = "DevSecOps"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}
resource "aws_security_group" "devops" {
  name        = "devops-server-sg"
  description = "Security group for DevSecOps infrastructure"
  vpc_id      = aws_vpc.devops.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "devops-server-sg"
    Project = "DevSecOps"
  }
}
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "state"
    values = ["available"]
  }
}

resource "aws_instance" "devops" {
  ami                         = data.aws_ami.amazon_linux.id
  instance_type               = "t3.micro"
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.devops.id]
  associate_public_ip_address = true

  tags = {
    Name    = "terraform-devops-server"
    Project = "DevSecOps"
  }
}
resource "aws_ebs_volume" "devops_data" {
  availability_zone = aws_instance.devops.availability_zone
  size              = 30
  type              = "gp3"
  encrypted         = true

  tags = {
    Name    = "devops-data-volume"
    Project = "DevSecOps"
  }
}
resource "aws_volume_attachment" "devops_data" {
  device_name = "/dev/sdf"
  volume_id   = aws_ebs_volume.devops_data.id
  instance_id = aws_instance.devops.id
}
