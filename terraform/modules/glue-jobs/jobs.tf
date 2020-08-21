locals {
  quantity = 3
  jobpath = "${path.module}/tmp/jobs"
}


resource "local_file" "my_glue_job" {
  filename = "${local.jobpath}/aiouti-job.py"
}

resource "aws_s3_bucket_object" "s3_iot_cert_pem" {
  bucket = "aiouti-lf"
  key    =  "lakeformation/measurements/job"
  source = local_file.my_glue_job.filename
}
