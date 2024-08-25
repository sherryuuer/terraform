# workspace 也是一种环境隔离的方法，感觉就像 Git 中的分支，将工作分离在不同的区域
# 但是最终 state 文件还是存储在同一个 s3 bucket 的不同文件夹，不能算是完全的隔离，最好的还是文件夹隔离的layout
# command:
# terraform workspace show
# terraform workspace list
# terraform workspace new name
# terraform workspace select

terraform {
  required_version = ">= 1.0.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  backend "s3" {

    # This backend configuration is filled in automatically at test time by Terratest. If you wish to run this example
    # manually, uncomment and fill in the config below.

    # bucket         = "<YOUR S3 BUCKET>"
    # key            = "<SOME PATH>/terraform.tfstate"
    # region         = "us-east-2"
    # dynamodb_table = "<YOUR DYNAMODB TABLE>"
    # encrypt        = true

  }
}

provider "aws" {
  region = "us-east-2"
}

resource "aws_instance" "example" {
  ami = "ami-0fb653ca2d3203ac1"

  instance_type = terraform.workspace == "default" ? "t2.medium" : "t2.micro"

}
