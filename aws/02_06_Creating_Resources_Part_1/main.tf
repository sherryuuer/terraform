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

# resource "<provider>_<resource_type>" "local_name" {
#   argument1 = value1
#   argument2 = value2
#   .....
# }


# Create a VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = {
    "Name" = "Main VPC"
  }
}
