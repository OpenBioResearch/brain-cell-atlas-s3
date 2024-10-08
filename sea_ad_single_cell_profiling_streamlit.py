"""
This script interacts with a publicly accessible AWS S3 bucket, summarizes bucket contents by file type, data source, file extension, and unique donor IDs, then displays this information in a Streamlit app.
"""

import boto3
import streamlit as st
from collections import Counter
from botocore import UNSIGNED
from botocore.client import Config

BUCKET_ARN = "arn:aws:s3:::sea-ad-single-cell-profiling"
bucket_name = BUCKET_ARN.rsplit(':', maxsplit=1)[-1]

# Initialize S3 client with unsigned config for public access
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

response = s3.list_objects_v2(Bucket=bucket_name)

# Counters for different aspects
file_extensions = Counter()
data_sources = Counter()
file_types = Counter()
donor_ids = set()

if 'Contents' in response:
    for obj in response["Contents"]:
        key = obj["Key"]
        parts = key.split("/")

        file_extensions[key.split(".")[-1].lower()] += 1

        if len(parts) >= 1 and parts[0] in ["DLPFC", "MTG"]:
            data_sources[parts[0]] += 1

        if len(parts) >= 2 and parts[1] in ["RNAseq", "ATACseq"]:
            file_types[parts[1]] += 1

        if "_SEAAD_" in key:
            donor_id = key.split("_SEAAD_")[0]
            donor_ids.add(donor_id)

def format_summary(summary_dict):
    formatted_text = ""
    for key, value in summary_dict.items():
        formatted_text += f"- {key}: {value}\n"
    return formatted_text

def create_streamlit_app(files, summaries):
    st.title("S3 Bucket File List and Summary")

    st.subheader("File Extension Summary")
    st.write(format_summary(summaries["file_extensions"]))

    st.subheader("Data Source Summary")
    st.write(format_summary(summaries["data_sources"]))

    st.subheader("File Type Summary")
    st.write(format_summary(summaries["file_types"]))

    st.subheader("Unique Donor IDs (if present)")
    st.write(len(summaries["donor_ids"]))

    st.header("File List")
    st.write(files)

    st.subheader("File Extensions Count")
    st.bar_chart(summaries["file_extensions"])

if __name__ == "__main__":
    response = s3.list_objects_v2(Bucket=bucket_name)
    files = [obj["Key"] for obj in response["Contents"]]

    summaries = {
        "file_extensions": file_extensions,
        "data_sources": data_sources,
        "file_types": file_types,
        "donor_ids": donor_ids,
    }

    create_streamlit_app(files, summaries)