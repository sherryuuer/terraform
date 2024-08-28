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

variable "users" {
  type = list(string)
  default = ["demo-user", "admin1", "john"]
}

resource "aws_iam_user" "test" {
  for_each = toset(var.users) # converts a list to a set
  name = each.key
}
