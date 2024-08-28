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

module "myec2" {
  # path to the module's directory
  source = "../modules/ec2"

  # module inputs
  ami_id = var.ami_id
  instance_type = var.instance_type
  servers = var.servers
}
