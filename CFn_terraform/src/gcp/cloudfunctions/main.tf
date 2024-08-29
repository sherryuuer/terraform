terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
  backend "gcs" {
    bucket = "oh-test"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "function_code_bucket" {
  name          = "gcf-v2-sources-${var.project_number}-${var.region}"
  location      = var.region
  force_destroy = true
}

resource "google_storage_bucket_object" "function_code" {
  name   = "sample_code.zip"
  bucket = google_storage_bucket.function_code_bucket.name
  source = "${path.module}/../../cloudfunctions/sample_code.zip"
}

resource "google_cloudfunctions_function" "function1" {
  name                  = "sample_function"
  runtime               = "python310"
  entry_point           = "main"
  source_archive_bucket = google_storage_bucket.function_code_bucket.name
  source_archive_object = google_storage_bucket_object.function_code.name
  trigger_http          = true
}
