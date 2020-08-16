module "network" {
  source         = "./modules/network"
  name           = var.name
  cidr           = var.cidr
  azs            = var.azs
  public_subnets = var.public_subnets
}

module "crawler" {
  source = "./modules/glue-crawlers"

  aws_region          = var.aws_region
  crawler_name        = var.crawler_name
  crawler_description = var.crawler_description
  crawler_role        = var.crawler_role
  data_source_path    = var.data_source_path
  database_name       = var.database_name
  table_prefix        = var.table_prefix
  schedule            = var.schedule
}
