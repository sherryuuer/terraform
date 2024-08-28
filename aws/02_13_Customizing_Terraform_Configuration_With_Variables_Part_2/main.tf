terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

# Configure the AWS Provider
# !!Use your own access and secret keys!!
provider "aws"{
  region     = "eu-central-1"
}

# Create a VPC
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr_block
  tags = {
    "Name" = "Production ${var.main_vpc_name}"  # string interpolation
  }
}

# Create a subnet in the VPC
resource "aws_subnet" "web"{
  vpc_id = aws_vpc.main.id
  cidr_block = var.web_subnet
  availability_zone = var.subnet_zone
  tags = {
    "Name" = "Web subnet"
  }
}
