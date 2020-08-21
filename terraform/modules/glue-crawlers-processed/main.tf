resource "aws_glue_crawler" "example" {
  database_name = "aiouti-db"
  name          = "aiouti_processed_crawler"
  role          = "arn:aws:iam::622305974757:role/aiouti-glue-role"
  schedule = "cron(0/10 * * * ? *)"

  s3_target {
    path = "s3://aiouti-lf/lakeformation/measurements/processed"
  }
}
