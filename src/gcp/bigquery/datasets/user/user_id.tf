module "user_id" {
  source     = var.module_source
  dataset_id = google_bigquery_dataset.user_dataset.dataset_id
  table_id   = "user_id"
  schema     = jsonencode([
    {
      "name": "id",
      "type": "INTEGER"
      "mode": "REQUIRED"
    },
    {
      "name": "user_id",
      "type": "INTEGER"
    },
    {
      "name": "modified",
      "type": "DATETIME",
      "mode": "REQUIRED"
    }
  ])

  time_partitioning = {
    type  = "DAY"
    field = "modified"
  }
  primary_key = ["id"]
}
