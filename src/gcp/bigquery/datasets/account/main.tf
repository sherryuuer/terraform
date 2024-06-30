resource "google_bigquery_dataset" "account_dataset" {
  dataset_id = "account"
  location   = var.region
}

# 这里引用modules的path总是出问题，不行就用resource直接定义也可以
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
