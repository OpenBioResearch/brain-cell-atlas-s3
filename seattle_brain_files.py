import boto3
from botocore import UNSIGNED
from botocore.client import Config

# AWS Open Data S3 ARN Details
bucket_arn = "arn:aws:s3:::sea-ad-single-cell-profiling"

# Extract bucket name from ARN
bucket_name = bucket_arn.split(":")[-1]

# Initialize S3 client with unsigned config for public access
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

# List objects in the bucket
response = s3.list_objects_v2(Bucket=bucket_name)

# Extract and print keys (file names)
if 'Contents' in response:
    for obj in response['Contents']:
        print(obj['Key'])
else:
    print("No objects found in the bucket.")
