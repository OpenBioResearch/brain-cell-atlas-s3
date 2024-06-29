import boto3
from collections import Counter
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

# Counters for different file types and data sources
file_extensions = Counter()
data_sources = Counter()  # E.g., DLPFC, MTG
file_types = Counter()  # E.g., RNAseq, ATACseq
donor_ids = set()  # Store unique donor IDs

# Iterate through objects
for obj in response["Contents"]:
    key = obj["Key"]
    parts = key.split("/")

    # File Extension
    ext = key.split(".")[-1].lower()
    file_extensions[ext] += 1

    # Data Source
    if len(parts) >= 1 and parts[0] in ["DLPFC", "MTG"]:
        data_sources[parts[0]] += 1

    # File Type
    if len(parts) >= 2 and parts[1] in ["RNAseq", "ATACseq"]:
        file_types[parts[1]] += 1

    # Donor ID (optional, if present in file names)
    if "_SEAAD_" in key:
        donor_id = key.split("_SEAAD_")[0]
        donor_ids.add(donor_id)

# Summary Output
print("\nFile Extension Summary:")
for ext, count in file_extensions.most_common():
    print(f"- {ext}: {count} files")

print("\nData Source Summary:")
for source, count in data_sources.most_common():
    print(f"- {source}: {count} files")

print("\nFile Type Summary:")
for file_type, count in file_types.most_common():
    print(f"- {file_type}: {count} files")

print("\nUnique Donor IDs (if present):", len(donor_ids))
