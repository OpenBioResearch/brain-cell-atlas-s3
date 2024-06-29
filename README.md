# alzheimers-research-s3

## Project Overview

This project includes three Python scripts that provide simple summaries for the Seattle Alzheimer's Disease Brain Cell Atlas (SEA-AD) dataset, which resides in a publicly accessible S3 bucket within the Registry of Open Data on AWS. The project also includes a visualization through a Streamlit website.

## Setup

The following libraries are required for this project:
- `boto3`
- `streamlit`

You can install these libraries using pip:

```bash
pip install -r requirements.txt
```

## Running the Scripts

### Listing Files:

```bash
python seattle_brain_files.py
```

### Generating Summary:

```bash
python seattle_brain_summary.py
```

### Running the Streamlit App:

```bash
streamlit run seattle_brain_streamlit.py
```

## License

This project is subject to the terms and conditions outlined at [Allen Institute Terms of Use](https://alleninstitute.org/legal/terms-use/).

## Datasets

The dataset used in this project is provided by the Seattle Alzheimer's Disease Brain Cell Atlas (SEA-AD) and is available in the [Registry of Open Data on AWS](https://registry.opendata.aws/).
