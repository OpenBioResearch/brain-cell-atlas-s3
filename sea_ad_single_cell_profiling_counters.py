"""This script provides a dataset overview of the Seatle Brain Cell Atlas S3 bucket, including h5ad (single-cell data) and bw (genomic data visualization) with data sourced from DLPFC (Dorsolateral Prefrontal Cortex) and MTG (Middle Temporal Gyrus) regions, primarily focused on ATACseq (chromatin accessibility) and RNAseq (gene expression) techniques. 
"""

import boto3
from collections import Counter
from botocore import UNSIGNED
from botocore.client import Config
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

def summarize_s3_bucket_contents(bucket_arn):
    # Counters
    try:
        bucket_name = bucket_arn.split(":")[-1]

        # Initialize S3 client with unsigned config for public access
        s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

        response = s3.list_objects_v2(Bucket=bucket_name)

        if 'Contents' not in response:
            print("No contents found in the bucket.")
            return None

        file_extensions = Counter()
        data_sources = Counter()  # E.g., DLPFC, MTG
        file_types = Counter()  # E.g., RNAseq, ATACseq
        donor_ids = set()  # unique donor IDs

        for obj in response["Contents"]:
            key = obj["Key"]
            parts = key.split("/")

            ext = key.split(".")[-1].lower()
            file_extensions[ext] += 1

            if len(parts) >= 1 and parts[0] in ["DLPFC", "MTG"]:
                data_sources[parts[0]] += 1

            if len(parts) >= 2 and parts[1] in ["RNAseq", "ATACseq"]:
                file_types[parts[1]] += 1

            # Donor ID (optional, if present in file names)
            if "_SEAAD_" in key:
                donor_id = key.split("_SEAAD_")[0]
                donor_ids.add(donor_id)

        summary = {
            "file_extensions": dict(file_extensions),
            "data_sources": dict(data_sources),
            "file_types": dict(file_types),
            "unique_donor_ids_count": len(donor_ids)
        }

        return summary

    except (NoCredentialsError, PartialCredentialsError) as e:
        print("Credentials error:", e)
    except ClientError as e:
        print("AWS Client error:", e)
    except Exception as e:
        print("An error occurred:", e)

    return None

bucket_arn = "arn:aws:s3:::sea-ad-single-cell-profiling"
summary = summarize_s3_bucket_contents(bucket_arn)

if summary:
    print("\nFile Extension Summary:")
    for ext, count in summary["file_extensions"].items():
        print(f"- {ext}: {count} files")

    print("\nData Source Summary:")
    for source, count in summary["data_sources"].items():
        print(f"- {source}: {count} files")

    print("\nFile Type Summary:")
    for file_type, count in summary["file_types"].items():
        print(f"- {file_type}: {count} files")

    print("\nUnique Donor IDs (if present):", summary["unique_donor_ids_count"])
else:
    print("Failed to summarize S3 bucket contents.")