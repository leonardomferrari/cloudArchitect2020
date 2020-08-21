locals {
  jobpath = "${path.module}/tmp/jobs"
}


resource "local_file" "my_glue_job" {
  filename = "${local.jobpath}/aiouti-job.py"
}

resource "aws_s3_bucket_object" "s3_my_glue_job_py" {
  bucket = "aiouti-lf"
  key    =  "lakeformation/measurements/job/aiouti"
  content = template_file.jobs_data.rendered
  etag = md5(template_file.jobs_data.rendered)
  //source = local_file.my_glue_job.filename
}
