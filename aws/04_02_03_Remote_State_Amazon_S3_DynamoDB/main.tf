terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

# Configure the AWS Provider
provider "aws"{
  region     = "eu-central-1"
  access_key = ""
  secret_key = ""
}

# Create an EC2 instance
resource "aws_instance" "server" {
  ami = "ami-05cafdf7c9f772ad2"
  instance_type = "t2.micro"
}
