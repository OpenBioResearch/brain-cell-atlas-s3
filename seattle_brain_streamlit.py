import boto3
import streamlit as st
from collections import Counter

"""
This script is designed to interact with a publicly accessible AWS S3 bucket. It retrieves a list of files,
summarizes them by file type, data source, file extension, and unique donor IDs, then displays this information in a Streamlit app.
"""

# AWS Open Data S3 ARN Details
bucket_arn = "arn:aws:s3:::sea-ad-single-cell-profiling"
bucket_name = bucket_arn.split(":")[-1]

# Initialize S3 client
s3 = boto3.client("s3")

# List objects in the bucket
response = s3.list_objects_v2(Bucket=bucket_name)

# Counters for different aspects
file_extensions = Counter()
data_sources = Counter()
file_types = Counter()
donor_ids = set()

# Iterate through objects and categorize
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


# Function to format the summary for Streamlit
def format_summary(summary_dict):
    formatted_text = ""
    for key, value in summary_dict.items():
        formatted_text += f"- {key}: {value}\n"
    return formatted_text


# Create the Streamlit app
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


# Main execution
if __name__ == "__main__":
    response = s3.list_objects_v2(Bucket=bucket_name)
    files = [obj["Key"] for obj in response["Contents"]]

    # Prepare all summaries in a dictionary
    summaries = {
        "file_extensions": file_extensions,
        "data_sources": data_sources,
        "file_types": file_types,
        "donor_ids": donor_ids,
    }

    create_streamlit_app(files, summaries)
