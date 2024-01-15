# Script folder

This folder contains utility scripts for the maintenance of the package.

## scrap_DICOM_fields.py

This script downloads a web page and tries to scrap the DICOM fields and their anonymization command from it.

1. Pull the repository: `git clone https://github.com/KitwareMedical/dicom-anonymizer.git`
1. Go in the repository: `cd dicom-anonymizer`
1. Install the dependencies: `pip install -e '.[dev]'`
1. Run the script: `python scripts/scrap_DICOM_fields.py` (Run it with `-h` to get a list of arguments)