## Creates a WAF IP Set to be used as a Blacklist for a WAF Rule to add to the Web ACL
## Value can be replaced with a Variable or a Static Value of an EIP within the customer VPC
## to test functionality of the WAF blocking access via IP
resource "aws_waf_ipset" "AWS_Security_Blog_Blacklist_IPSet" {
  name = var.AWS_Security_Blog_Blacklist_IPSet_Name
  ip_set_descriptors {
    type  = "IPV4"
    value = "10.0.0.99/32"
  }
}
## Creates SQL Injection match condition with multiple filters based on AWS best practices
## reccomendations from the Mitigated OWASP Top 10 with AWS WAF White Paper
resource "aws_waf_sql_injection_match_set" "AWS_Security_Blog_SQLI_Match_Set" {
  name = var.AWS_Security_Blog_SQLI_Match_Set_Name
  sql_injection_match_tuples {
    text_transformation = "HTML_ENTITY_DECODE"
    field_to_match {
      type = "QUERY_STRING"
    }
  }
  sql_injection_match_tuples {
    text_transformation = "URL_DECODE"
    field_to_match {
      type = "QUERY_STRING"
    }
  }
  sql_injection_match_tuples {
    text_transformation = "HTML_ENTITY_DECODE"
    field_to_match {
      type = "URI"
    }
  }
  sql_injection_match_tuples {
    text_transformation = "URL_DECODE"
    field_to_match {
      type = "URI"
    }
  }
  sql_injection_match_tuples {
    text_transformation = "HTML_ENTITY_DECODE"
    field_to_match {
      type = "BODY"
    }
  }
  sql_injection_match_tuples {
    text_transformation = "URL_DECODE"
    field_to_match {
      type = "BODY"
    }
  }
  sql_injection_match_tuples {
    text_transformation = "HTML_ENTITY_DECODE"
    field_to_match {
      type = "HEADER"
      data = "Cookie"
    }
  }
  sql_injection_match_tuples {
    text_transformation = "URL_DECODE"
    field_to_match {
      type = "HEADER"
      data = "Cookie"
    }
  }
  sql_injection_match_tuples {
    text_transformation = "HTML_ENTITY_DECODE"
    field_to_match {
      type = "HEADER"
      data = "Authorization"
    }
  }
  sql_injection_match_tuples {
    text_transformation = "URL_DECODE"
    field_to_match {
      type = "HEADER"
      data = "Authorization"
    }
  }
}
