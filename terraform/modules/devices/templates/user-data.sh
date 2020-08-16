#!/bin/bash

mkdir ~/cert
aws s3 cp s3://aiouti-lf/certs/certificate.cert.pem ~/cert/certificate.cert.pem
aws s3 cp s3://aiouti-lf/certs/certificate.public.key ~/cert/certificate.public.key
aws s3 cp s3://aiouti-lf/certs/certificate.private.key ~/cert/certificate.private.key

# ECS config
{
  echo "ECS_CLUSTER=${cluster_name}"
} >> /etc/ecs/ecs.config

start ecs

echo "Done"
