############################
## main.tf Variables ##
############################
variable "allowed_account_ids" {
  description = "List of allowed AWS account ids where resources can be created"
  default     = []
}

variable "name" {
  description = "Name to be used on all the resources as identifier"
  default     = ""
}

variable "cidr" {
  description = "The CIDR block for the VPC. Default value is a valid CIDR, but not acceptable by AWS and should be overriden"
  default     = "0.0.0.0/0"
}

variable "azs" {
  description = "A list of availability zones in the region"
  default     = []
}

variable "public_subnets" {
  description = "A list of public subnets inside the VPC"
  default     = []
}

#######################################
## main.tf Variables for Glue Crawler ##
#######################################

variable "aws_region" {
  description = "AWS Region"
  default     = "us-east-1"
}

variable "crawler_name" {
  description = "Crawler Name"
  default     = "aiouti-crawler"
}

variable "crawler_description" {
  description = "Crawler Description"
  default     = "Managed by TerraHub"
}

variable "crawler_role" {
  description = "Crawler Role"
  default     = "arn:aws:iam::622305974757:role/aiouti-lf-stack-CFNGlueServiceMLLabRole-6Q9PXU7FSXLM"
}

variable "data_source_path" {
  description = "S3 Source Path"
  default     = "s3://aiouti-lf/lakeformation"
}

variable "database_name" {
  description = "Database Name"
  default     = "aiouti-db"
}

variable "table_prefix" {
  description = "Table Prefix"
  default     = ""
}

variable "schedule" {
  description = "Schedule, a cron expression in form of cron(15 12 * * ? *) "
  default     = "cron(0/10 * ? * MON-FRI *)"
}
