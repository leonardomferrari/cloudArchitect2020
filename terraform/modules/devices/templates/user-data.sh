#!/bin/bash

cd /home
cd ec2-user
mkdir cert
cd cert
aws s3 cp s3://aiouti-lf/certs/certificate.cert.pem certificate.cert.pem
aws s3 cp s3://aiouti-lf/certs/certificate.public.key certificate.public.key
aws s3 cp s3://aiouti-lf/certs/certificate.private.key certificate.private.key
wget https://www.amazontrust.com/repository/AmazonRootCA1.pem -o certificate.root.pem

# ECS config
{
  echo "ECS_CLUSTER=${cluster_name}"
} >> /etc/ecs/ecs.config

start ecs

echo "Done"
