import boto3
from botocore import UNSIGNED
from botocore.client import Config

def list_s3_objects(bucket_arn):
    """
    Simple SEA-AD S3 bucket list. AWS has now created a bucket browser.
    """
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
    for obj in objects:
        print(obj)
else:
    print("No objects found in the bucket.")
