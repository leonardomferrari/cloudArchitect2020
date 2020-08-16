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
  count = 3
  active = true
}

resource "aws_s3_bucket_object" "s3_certs_folders" {
  count = 3
  bucket = "aiouti-lf"
  key    = "certs-${count.index}/"
}

resource "local_file" "iot_cert_pem" {
  count = 3
  sensitive_content = aws_iot_certificate.cert[count.index].certificate_pem
  filename = "${path.module}/devices/certs/cert-${count.index}/certificate.cert.pem"
}

resource "aws_s3_bucket_object" "s3_iot_cert_pem" {
  count = 3
  bucket = "aiouti-lf"
  key    = "certs-${count.index}/certificate.cert.pem"
  source = "${path.module}/devices/certs/cert-${count.index}/certificate.cert.pem"
  etag   = fileexists(local_file.cert_public_key[count.index].filename) ? filemd5(local_file.iot_cert_pem[count.index].filename) : md5("None")
}

resource "local_file" "cert_public_key" {
  count = 3
  sensitive_content = aws_iot_certificate.cert[count.index].public_key
  filename = "${path.module}/devices/certs/cert-${count.index}/certificate.public.key"
}

resource "aws_s3_bucket_object" "s3_cert_public_key" {
  count = 3
  bucket = "aiouti-lf"
  key    = "certs-${count.index}/certificate.public.key"
  source = "${path.module}/devices/certs/cert-${count.index}/certificate.public.key"
  etag   = fileexists(local_file.cert_public_key[count.index].filename) ? filemd5(local_file.cert_public_key[count.index].filename) : md5("None")
}

resource "local_file" "cert_private_key" {
  count = 3
  sensitive_content = aws_iot_certificate.cert[count.index].private_key
  filename = "${path.module}/devices/certs/cert-${count.index}/certificate.private.key"
}

resource "aws_s3_bucket_object" "s3_cert_private_key" {
  count = 3
  bucket = "aiouti-lf"
  key    = "certs-${count.index}/certificate.private.key"
  source = "${path.module}/devices/certs/cert-${count.index}/certificate.private.key"
  etag   = fileexists(local_file.cert_public_key[count.index].filename) ? filemd5(local_file.cert_private_key[count.index].filename) : md5("None")
}

resource "aws_iot_policy_attachment" "att-policy" {
  count = 3
  policy = aws_iot_policy.iot_policy.name
  target = aws_iot_certificate.cert[count.index].arn
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
  principal = aws_iot_certificate.cert[count.index].arn
  thing = aws_iot_thing.thing[count.index].name
}





