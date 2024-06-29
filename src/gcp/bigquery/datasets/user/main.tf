provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_bigquery_dataset" "user_dataset" {
  dataset_id = "user"
  location   = var.region
}
