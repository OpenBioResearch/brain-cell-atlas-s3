import pandas as pd
import boto3

# AWS Open Data S3 ARN Details
bucket_arn = "arn:aws:s3:::sea-ad-single-cell-profiling"

# Extract bucket name from ARN
bucket_name = bucket_arn.split(":")[-1]

# Initialize S3 client (no credentials needed for public buckets)
s3 = boto3.client("s3")

# List objects in the bucket
response = s3.list_objects_v2(Bucket=bucket_name)

# Extract and print keys (file names)
for obj in response["Contents"]:
    print(obj["Key"])
