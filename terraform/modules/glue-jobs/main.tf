resource "aws_glue_job" "example" {
  name     = var.job_name
  role_arn = var.job_role

  command {
    script_location = "${var.job_script_location}/aiouti"
  }
}
