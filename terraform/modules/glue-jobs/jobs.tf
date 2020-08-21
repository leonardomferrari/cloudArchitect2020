locals {
  jobpath = "${path.module}/tmp/jobs"
}


resource "local_file" "my_glue_job" {
  filename = "${local.jobpath}/aiouti-job.py"
}

resource "aws_s3_bucket_object" "aiouti_python_job" {
  bucket = "aiouti-lf"
  key    =  "lakeformation/measurements/job/aiouti-job.py"
  source = local_file.my_glue_job.filename
}
