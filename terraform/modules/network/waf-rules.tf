## Creates an AWS WAF Rule to Blacklist the IP Address specified in the IPSet Condition
resource "aws_waf_rule" "AWS_Security_Blog_IP_Blacklist_Rule" {
  name        = var.AWS_Security_Blog_IP_Blacklist_Rule_Name
  metric_name = var.AWS_Security_Blog_IP_Blacklist_Rule_Name
  predicates {
    data_id = aws_waf_ipset.AWS_Security_Blog_Blacklist_IPSet.id
    negated = false
    type    = "IPMatch"
  }
}

## Creates an AWS WAF Rule matched against Conditions listed in the SQL Injection Condition Match Set
resource "aws_waf_rule" "AWS_Security_Blog_SQL_Injection_Rule" {
  name        = var.AWS_Security_Blog_SQL_Injection_Rule_Name
  metric_name = var.AWS_Security_Blog_SQL_Injection_Rule_Name
  predicates{
    data_id = aws_waf_sql_injection_match_set.AWS_Security_Blog_SQLI_Match_Set.id
    negated = false
    type = "SqlInjectionMatch"
  }
}

## Creates an AWS WAF Web ACL that will Block traffic originating from the Blacklist, as well as block traffic
## that matches any SQL Injection methods. Logs are sent to a Kinesis Data Firehose for further processing and investigation
resource "aws_waf_web_acl" "AWS_Security_Blog_Blacklist_WACL" {
  name        = var.AWS_Security_Blog_Blacklist_WACL_Name
  metric_name = var.AWS_Security_Blog_Blacklist_WACL_Name
  default_action {
    type = "ALLOW"
  }
  rules {
    action {
      type = "BLOCK"
    }
    priority = 1
    rule_id  = aws_waf_rule.AWS_Security_Blog_SQL_Injection_Rule.id
    type     = "REGULAR"
  }
  rules {
    action {
      type = "BLOCK"
    }
    priority = 2
    rule_id  = aws_waf_rule.AWS_Security_Blog_IP_Blacklist_Rule.id
    type     = "REGULAR"
  }
}
