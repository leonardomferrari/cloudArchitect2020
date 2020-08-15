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
  type        = "list"
  default     = []
}

variable "public_subnets" {
  description = "A list of public subnets inside the VPC"
  type        = "list"
  default     = []
}

#################################
## waf-conditions.tf Variables ##
#################################
variable "AWS_Security_Blog_Blacklist_IPSet_Name" {
  default = "devsecopsblacklistipset"
}
variable "AWS_Security_Blog_SQLI_Match_Set_Name" {
  default = "devsecopssqlimatchset"
}

############################
## waf-rules.tf Variables ##
############################
variable "AWS_Security_Blog_IP_Blacklist_Rule_Name" {
  default = "devsecopsblacklistrule"
}
variable "AWS_Security_Blog_SQL_Injection_Rule_Name" {
  default = "devsecopssqlirule"
}
variable "AWS_Security_Blog_Blacklist_WACL_Name" {
  default = "devsecopswebacl"
}
