provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_bigquery_dataset" "account_dataset" {
  dataset_id = "account"
  location   = var.region
}

module "accountid" {
  source     = "../../../modules/bigquery_table"
  dataset_id = google_bigquery_dataset.account_dataset.dataset_id
  table_id   = "accountid"
  schema     = jsonencode([
    {
      "name": "account_id",
      "type": "INTEGER"
    },
    {
      "name": "user_id",
      "type": "INTEGER"
    }
  ])
}

module "accountdetail" {
  source     = "../../../modules/bigquery_table"
  dataset_id = google_bigquery_dataset.account_dataset.dataset_id
  table_id   = basename(abspath(path.module))
  schema     = jsonencode([
    {
      "name": "account_id",
      "type": "INTEGER"
    },
    {
      "name": "details",
      "type": "STRING"
    }
  ])
}
