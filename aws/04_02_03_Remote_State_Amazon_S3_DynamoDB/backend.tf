terraform {
  backend "s3" {
    bucket = "masterterraform"  # should already exist on AWS S3
    key    = "s3_backend.tfstate"
    dynamodb_table = "s3-state-lock"  # should already exist on AWS

    region = "eu-central-1"
    access_key = ""
    secret_key = ""
  }
}
