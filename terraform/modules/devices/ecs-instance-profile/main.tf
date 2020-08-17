resource "aws_iam_role" "this" {
  name = "${var.name}_ecs_instance_role"
  path = "/ecs/"

  assume_role_policy = <<EOF
{
  "Version": "2008-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": ["ec2.amazonaws.com"]
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "aiouti-device-certs" {
  name        = "aiouti-certs-policy"
  path        = "/"
  description = "Provides de test devices access to the certs"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::aiouti-lf/certs*"
            ]
        }
    ]
}
EOF
}

resource "aws_iam_policy" "aiouti-device-log" {
  name        = "aiouti-device-log"
  path        = "/"
  description = "Provides access to login functionality"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": {
        "Effect": "Allow",
        "Action": [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:DescribeLogGroups",
            "logs:DescribeLogStreams",
            "logs:PutLogEvents",
            "logs:GetLogEvents",
            "logs:FilterLogEvents"
        ],
        "Resource": "arn:aws:logs:*:*:*"
    }
}
EOF
}

resource "aws_iam_instance_profile" "this" {
  name = "${var.name}_ecs_instance_profile"
  role = aws_iam_role.this.name
}

resource "aws_iam_role_policy_attachment" "ecs_device_certs" {
  role       = aws_iam_role.this.id
  policy_arn = aws_iam_policy.aiouti-device-certs.arn
}

resource "aws_iam_role_policy_attachment" "ecs_device_log" {
  role       = aws_iam_role.this.id
  policy_arn = aws_iam_policy.aiouti-device-log.arn
}

resource "aws_iam_role_policy_attachment" "ecs_ec2_role" {
  role       = aws_iam_role.this.id
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_role_policy_attachment" "ecs_ec2_cloudwatch_role" {
  role       = aws_iam_role.this.id
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
}
