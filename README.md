# brain-cell-atlas-s3

## Project Overview

This project provides Python scripts and a Streamlit web application to enhance exploration of the  SEA-AD dataset publicly hosted on AWS. The SEA-AD project is an initiative to understand the molecular and cellular changes underlying Alzheimer's disease (AD). By leveraging single-cell profiling technologies (snRNAseq and snATAC-seq), researchers gain insights into the gene expression and epigenomic landscapes of both diseased and healthy brains.

Why This Project?

The raw SEA-AD dataset is vast, so this project aims to summarize the data types and distribution of bucket objects, to provide a Streamlit app for easy visualization and a few foundational python scripts to modify retrieved bucket objects.

## Setup

**Clone the repository:**

```bash
git clone https://github.com/OpenBioResearch/brain-cell-atlas-s3.git
cd brain-cell-atlas-s3
```

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
python sea_ad_single_cell_profiling_files.py
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
