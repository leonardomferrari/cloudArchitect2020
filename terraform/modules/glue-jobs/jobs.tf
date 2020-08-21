locals {
  quantity = 3
  jobpath = "${path.module}/tmp/jobs"
}


resource "local_file" "my_glue_job" {
  filename = "${local.jobpath}/aiouti.py"
}

resource "aws_s3_bucket_object" "s3_iot_cert_pem" {
  bucket = "aiouti-lf"
  key    =  "aiouti"
  source = local_file.my_glue_job.filename
}















resource "aws_iot_policy" "iot_policy" {
  name = var.iot_policy
  policy = data.template_file.tf_iot_policy.rendered
}




resource "aws_s3_bucket_object" "s3_folder_folder" {
  bucket = "aiouti-lf"
  key    = "lakeformation/measurements/job/"
}

resource "aws_s3_bucket_object" "s3_cert_private_key" {
  bucket = "aiouti-lf"
  key    = "lakeformation/measurements/job/aiuoti"
  source = local_file.cert_private_key.filename
}

resource "local_file" "iot_cert_pem" {
  sensitive_content = aws_iot_certificate.cert.certificate_pem
  filename = "${local.certspath}/certificate.cert.pem"
}






resource "aws_s3_bucket_object" "s3_iot_cert_pem" {
  bucket = "aiouti-lf"
  key    = "certs/certificate.cert.pem"
  source = local_file.iot_cert_pem.filename
}

resource "local_file" "cert_public_key" {
  sensitive_content = aws_iot_certificate.cert.public_key
  filename = "${local.certspath}/certificate.public.key"
}

resource "aws_s3_bucket_object" "s3_cert_public_key" {
  bucket = "aiouti-lf"
  key    = "certs/certificate.public.key"
  source = local_file.cert_public_key.filename
}

resource "local_file" "cert_private_key" {
  sensitive_content = aws_iot_certificate.cert.private_key
  filename = "${local.certspath}/certificate.private.key"
}

resource "aws_iot_policy_attachment" "att-policy" {
  policy = aws_iot_policy.iot_policy.name
  target = aws_iot_certificate.cert.arn
}

resource "aws_iot_thing" "thing" {
  count = local.quantity
  name = "aiouti-thing-${count.index}"
  thing_type_name = aws_iot_thing_type.fs-type.name

  attributes = {
    First = "aiouti-thing-${count.index}-"
  }
}

resource "aws_iot_thing_principal_attachment" "att-thing" {
  count = local.quantity
  principal = aws_iot_certificate.cert.arn
  thing = aws_iot_thing.thing[count.index].name
}





