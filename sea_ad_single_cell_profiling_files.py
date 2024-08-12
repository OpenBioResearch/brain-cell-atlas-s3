"""
Lists object in the AWS S3 bucket using an unsigned request,
and saves the keys to a CSV file.
"""

import boto3
from botocore import UNSIGNED
from botocore.client import Config
import csv

def list_s3_objects(bucket_arn):
    try:
        bucket_name = bucket_arn.split(":")[-1]
        s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            return [obj['Key'] for obj in response['Contents']]
        else:
            return []
    except Exception as e:
        print(f"Error accessing bucket: {e}")
        return []

bucket_arn = "arn:aws:s3:::sea-ad-single-cell-profiling"
objects = list_s3_objects(bucket_arn)

if objects:
    with open('s3_objects_list.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Object Key"])
        for obj in objects:
            writer.writerow([obj])
    print("CSV file has been created successfully.")
else:
    print("No objects found in the bucket.")
