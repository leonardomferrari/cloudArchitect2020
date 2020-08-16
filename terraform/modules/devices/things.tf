resource "aws_iot_policy" "iot_policy" {
  name = var.iot_policy
  policy = data.template_file.tf_iot_policy.rendered
}

resource "aws_iot_thing_type" "fs-type" {
  name = "FS-15"
}
resource "aws_iot_thing_type" "lf-type" {
  name = "LF-10"
}
resource "aws_iot_thing_type" "pp-type" {
  name = "PP-5"
}

resource "aws_iot_certificate" "cert" {
  active = true
}

resource "aws_s3_bucket_object" "s3_certs_folder" {
  bucket = "aiouti-lf"
  key    = "certs/"
}

resource "local_file" "iot_cert_pem" {
  sensitive_content = aws_iot_certificate.cert.certificate_pem
  filename = "${path.module}/devices/certs/certificate.cert.pem"
}

resource "aws_s3_bucket_object" "s3_iot_cert_pem" {
  bucket = "aiouti-lf"
  key    = "certs/certificate.cert.pem"
  source = local_file.iot_cert_pem.filename
}

resource "local_file" "cert_public_key" {
  sensitive_content = aws_iot_certificate.cert.public_key
  filename = "${path.module}/devices/certs/certificate.public.key"
}

resource "aws_s3_bucket_object" "s3_cert_public_key" {
  bucket = "aiouti-lf"
  key    = "certs/certificate.public.key"
  source = local_file.cert_public_key.filename
}

resource "local_file" "cert_private_key" {
  sensitive_content = aws_iot_certificate.cert.private_key
  filename = "${path.module}/devices/certs/certificate.private.key"
}

resource "aws_s3_bucket_object" "s3_cert_private_key" {
  bucket = "aiouti-lf"
  key    = "certs/certificate.private.key"
  source = local_file.cert_private_key.filename
}

resource "aws_iot_policy_attachment" "att-policy" {
  policy = aws_iot_policy.iot_policy.name
  target = aws_iot_certificate.cert.arn
}

resource "aws_iot_thing" "thing" {
  count = 3
  name = "thing-${count.index}"
  thing_type_name = aws_iot_thing_type.fs-type.name

  attributes = {
    First = "thing-${count.index}-"
  }
}

resource "aws_iot_thing_principal_attachment" "att-thing" {
  count = 3
  principal = aws_iot_certificate.cert.arn
  thing = aws_iot_thing.thing[count.index].name
}





