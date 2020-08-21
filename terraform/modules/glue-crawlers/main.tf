# Updated because of https://www.terraform.io/upgrade-guides/0-13.html#destroy-time-provisioners-may-not-refer-to-other-resources
resource "null_resource" "crawler" {

  triggers = {
    module = path.module
    crawler_name = var.crawler_name
    aws_region = var.aws_region
  }

  provisioner "local-exec" {
    when    = create

    command = "touch ${self.triggers.module}/scripts/create.lock"
  }

  provisioner "local-exec" {
    when    = destroy

    command = "python ${self.triggers.module}/scripts/destroy.py ${self.triggers.crawler_name} ${self.triggers.aws_region}"
  }
}
