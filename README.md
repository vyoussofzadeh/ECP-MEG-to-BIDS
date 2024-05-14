# ECP-MEG-BIDS-Converter

This repository contains scripts and tools designed to convert MEG datasets from the Epilepsy Connectome Project (ECP) into the Brain Imaging Data Structure (BIDS) format. The goal is to provide a standardized approach for handling neuroimaging data to facilitate research and analysis.

## Project Description

The Epilepsy Connectome Project aims to advance our understanding of epilepsy through detailed imaging studies. The magnetoencephalography (MEG) data offers rich, dynamic insights into brain activity. Converting this data into BIDS format standardizes the data structure, making it more accessible and interoperable for researchers across various disciplines.

## Features

- **Script to Convert Data**: Automate the conversion of ECP MEG data to BIDS format.
- **Validation Tool**: Ensure that the converted data adheres to BIDS specifications.
- **Documentation**: Detailed instructions and examples on how to use the tools and scripts.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Required Python packages: `numpy`, `mne`, `pybids`

### Installation

Create a conda environment with the required programs:
```
conda create -n bids_conv -c conda-forge mne mne-bids pandas "python<3.12" -y 
```

Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/ECP-MEG-BIDS-Converter.git
```

## Usage

To convert data, run the conversion script from the command line:
```
#Set the Daysback variable in bash before running - this will be pulled in from the code
#Do not set this in github code or you will de-anonymize the date of your data
export BIDS_DAYSBACK=????
```

```bash
python convert_to_bids.py <input_file> <output_directory>
