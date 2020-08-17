resource "aws_cloudwatch_log_group" "aiouti-device" {
  name              = "aiouti-device"
  retention_in_days = 1
}

resource "aws_ecs_task_definition" "aiouti-device" {
  family = "aiouti-device"

  volume {
    host_path = "/ec2-user/cert"
    name = "certificatesvol"
  }

  container_definitions = <<EOF
[
  {
    "name": "aiouti-device",
    "image": "pablojulianperalta/aiouti-device:1.5",
    "cpu": 0,
    "memory": 128,
    "environment": [
      {
        "name": "IOT_URI",
        "value": "a4pefh4s7d44l-ats.iot.us-east-1.amazonaws.com"
      }
    ],
    "mountPoints": [
      {
        "sourceVolume": "certificatesvol",
        "containerPath": "/usr/src/app/cert",
        "readOnly": true
      }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-region": "us-east-1",
        "awslogs-group": "aiouti-device",
        "awslogs-stream-prefix": "complete-ecs"
      }
    }
  }
]
EOF
}

resource "aws_ecs_service" "aiouti-device" {
  name            = "aiouti-device"
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.aiouti-device.arn

  desired_count = 5

  deployment_maximum_percent         = 100
  deployment_minimum_healthy_percent = 0
}
