import boto3
import os
import json
import datetime

s3_client = boto3.client('s3')


def lambda_handler(event, context):
  print("Received event: " + json.dumps(event, indent=2))

  S3_BUCKET = os.environ["S3_BUCKET"]
  bucket = S3_BUCKET if S3_BUCKET else 's3://aiouti-lf/lakeformation' \
                                       '/measurements/raw/ '
  date = datetime.datetime.strptime(event['date'], '%d-%m-%YT%H:%M:%S%z').timestamp()
  key = event['group'] + '/' + event['device'] + '/' + date + '.json'
  s3_client.upload_file(event, bucket, key)
