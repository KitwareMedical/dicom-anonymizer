# Installation

### Binary installation

Installation can be done via pip `pip install dicom-anonymizer` or conda `conda install -c conda-forge dicom-anonymizer`.


### Local Development Setup

To get started with local development, follow these steps:

1. Create a Virtual Environment:
   - On Windows:
     ```sh
     virtualenv env
     .\env\Scripts\activate.bat
     ```
   - On MacOS/Linux:
     ```sh
     python -m venv env
     source env/bin/activate
     ```

2. Install Dependencies:
   - Install an editable version of the package and the development requirements:
     ```sh
     pip install -e .[dev]
     ```

3. Set Up Pre-Commit Hooks:
   - Install the pre-commit hooks to ensure code quality:
     ```sh
     pre-commit install
     ```


## Testing

To run the unit tests, use the following command:

```sh
pytest
```


## Building

These instructions rely on wheel build-package format. Install it if you have not done it already using:
`pip install wheel`

The sources files can be packaged by using:
`python ./setup.py bdist_wheel`

This command will generate a wheel package in `dist` folder which can be then installed as a python package using
`pip install ./dist/dicom_anonymizer-1.0.13-1-py2.py3-none-any.whl`

On Windows, if you see a warning message
`'./dist/dicom_anonymizer-1.0.13-1-py2.py3-none-any.whl' looks like a filename, but the file does not exist`,
this could be due to pip not being able to handle relative path (See issue https://github.com/pypa/pip/issues/10808). As a work-around, change directory to `dist` and then install it using
`pip install dicom_anonymizer-1.0.13-1-py2.py3-none-any.whl`


Installing this package will also install an executable named `dicom-anonymizer`. In order to use it, please refer to the next section.
