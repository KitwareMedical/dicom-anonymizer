# DicomAnonymizer

Python package to anonymize DICOM files.
The anonymization answer to the standard . More information about dicom fields for anonymization can be found [here](https://dicom.nema.org/medical/dicom/current/output/html/part15.html#table_E.1-1).

The default behaviour of this package is to anonymize DICOM fields referenced in the 2023e DICOM standard. These fields are referenced in [dicomfields](dicomanonymizer/dicom_anonymization_databases/dicomfields_2023.py).  
Another standard can be selected, see *Change the DICOM anonymization standard*. 

Dicom fields are separated into different groups. Each groups will be anonymized in a different way.

| Group | Action | Action definition |
| --- | --- | --- |
| D_TAGS | replace | Replace with a non-zero length value that may be a dummy value and consistent with the VR** |
| Z_TAGS | empty | Replace with a zero length value, or a non-zero length value that may be a dummy value and consistent with the VR** |
| X_TAGS | delete | Completely remove the tag |
| U_TAGS | replace_UID | Replace all UID's random ones. Same UID will have the same replaced value |
| Z_D_TAGS | empty_or_replace | Replace with a non-zero length value that may be a dummy value and consistent with the VR** |
| X_Z_TAGS | delete_or_empty | Replace with a zero length value, or a non-zero length value that may be a dummy value and consistent with the VR** |
| X_D_TAGS | delete_or_replace | Replace with a non-zero length value that may be a dummy value and consistent with the VR** |
| X_Z_D_TAGS | delete_or_empty_or_replace | Replace with a non-zero length value that may be a dummy value and consistent with the VR** |
| X_Z_U_STAR_TAGS | delete_or_empty_or_replace_UID | If it's a UID, then all numbers are randomly replaced. Else, replace with a zero length value, or a non-zero length value that may be a dummy value and consistent with the VR**|
| ALL_TAGS | | Contains all previous defined tags


# How to install it?

Installation can be done via pip `pip install dicom-anonymizer` or conda `conda install -c conda-forge dicom-anonymizer`.


# Local Development Setup

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


## How to test it?

To run the unit tests, use the following command:

```sh
pytest
```


# How to build it?
These instructions rely on wheel build-package format. Install it if you have not done it already using:
`pip install wheel`

The sources files can be packaged by using:
`python ./setup.py bdist_wheel`

This command will generate a wheel package in `dist` folder which can be then installed as a python package using
`pip install ./dist/dicom_anonymizer-1.0.13-py2.py3-none-any.whl`

On Windows, if you see a warning message
`'./dist/dicom_anonymizer-1.0.13-py2.py3-none-any.whl' looks like a filename, but the file does not exist`,
this could be due to pip not being able to handle relative path (See issue https://github.com/pypa/pip/issues/10808). As a work-around, change directory to `dist` and then install it using
`pip install dicom_anonymizer-1.0.13-py2.py3-none-any.whl`


Installing this package will also install an executable named `dicom-anonymizer`. In order to use it, please refer to the next section.



# How to use it?

This package allows to anonymize a selection of DICOM field (defined or overridden).
The way on how the DICOM fields are anonymized can also be overridden.

- **[required]** InputPath = Full path to a single DICOM image or to a folder which contains dicom files
- **[required]** OutputPath = Full path to the anonymized DICOM image or to a folder. This folder has to exist.
- [optional] ActionName = Defined an action name that will be applied to the DICOM tag.
- [optional] Dictionary = Path to a JSON file which defines actions that will be applied on specific dicom tags (see below)



## Default behaviour

You can use the default anonymization behaviour describe above.

```python
dicom-anonymizer Input Output
```


## Private tags

Default behavior of the dicom anonymizer is to delete private tags.
But you can bypass it:
- Solution 1: Use regexp to define which private tag you want to keep/update (cf [custom rules](#custom-rules))
- Solution 2: Use dicom-anonymizer.exe option to keep all private tags : `--keepPrivateTags`



## Custom rules
You can manually add new rules in order to have different behaviors with certain tags.
This will allow you to override default rules:

**Executable**:
```python
dicom-anonymizer InputFilePath OutputFilePath -t '(0x0001, 0x0001)' ActionName -t '(0x0001, 0x0005)' ActionName2
```
This will apply the `ActionName` to the tag `'(0x0001, 0x0001)'` and `ActionName2` to `'(0x0001, 0x0005)'`

**Note**: ActionName has to be defined in [actions list](#actions-list)

Example 1: The default behavior of the patient's ID is to be replaced by an empty or null value. If you want to keep this value, then you'll have to run :
```python
python anonymizer.py InputFilePath OutputFilePath -t '(0x0010, 0x0020)' keep
```
This command will override the default behavior executed on this tag and the patient's ID will be kept.

Example 2: We just want to change the study date from 20080701 to 20080000, then we'll use the regexp
```python
python anonymizer.py InputFilePath OutputFilePath -t '(0x0008, 0x0020)' 'regexp' '0701$' '0000'
```

Example 3: Change the tag value with an arbitrary value
```python
python anonymizer.py InputFilePath OutputFilePath -t '(0x0010, 0x0010)' 'replace_with_value' 'new_value'
```

### DICOMDIR

> DICOMDIR anonymization is not specified. It is therefore discouraged and it is recommended to regenerate new DICOMDIR files after anonymizing the original DICOM files.

DICOMDIR files can have a `(0x0004, 0x1220)  Directory Record Sequence` tag that can contain patient information.  
However, this tag is not part of the standard tag to anonymize set. If you still want dicom-anonymizer to anonymize it, you have to instruct it explicitly:

```python
python anonymizer.py InputFilePath OutputFilePath -t '(0x0004, 0x1220)' replace
```

## Custom rules with dictionary file

Instead of having a big command line with several new actions, you can create your own dictionary by creating a json file `dictionary.json` :
```json
{
    "(0x0002, 0x0002)": "ActionName",
    "(0x0003, 0x0003)": "ActionName",
    "(0x0004, 0x0004)": "ActionName",
    "(0x0005, 0x0005)": "ActionName"
}
```
Same as before, the `ActionName` has to be defined in the [actions list](#actions-list).

```python
dicom-anonymizer InputFilePath OutputFilePath --dictionary dictionary.json
```

If you want to use the **regexp** action in a dictionary:
```json
{
    "(0x0002, 0x0002)": "ActionName",
    "(0x0008, 0x0020)": {
        "action": "regexp",
        "find": "0701$",
        "replace": "0000"
    }
}
```

## Custom/overrides actions

Here is a small example which keeps all metadata but updates the series description
by adding a suffix passed as a parameter.

```python
import argparse
from dicomanonymizer import ALL_TAGS, anonymize, keep


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        "input",
        help="Path to the input dicom file or input directory which contains dicom files",
    )
    parser.add_argument(
        "output",
        help="Path to the output dicom file or output directory which will contains dicom files",
    )
    args = parser.parse_args()

    deletePrivateTags = False

    input_dicom_path = args.input
    output_dicom_path = args.output

    extra_anonymization_rules = {}

    # Per https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html
    # it is all right to retain only the year part of the birth date for
    # de-identification purposes.
    def set_date_to_year(dataset, tag):
        element = dataset.get(tag)
        if element is not None:
            element.value = f"{element.value[:4]}0101" # YYYYMMDD format

    # ALL_TAGS variable is defined on file dicomfields.py
    # the 'keep' method is already defined into the dicom-anonymizer
    # It will overrides the default behaviour
    for i in ALL_TAGS:
        extra_anonymization_rules[i] = keep

    extra_anonymization_rules[(0x0010, 0x0030)] = set_date_to_year # Patient's Birth Date

    # Launch the anonymization
    anonymize(
        input_dicom_path,
        output_dicom_path,
        extra_anonymization_rules,
        delete_private_tags=False,
    )


if __name__ == "__main__":
    main()
```

See the full application in the `examples` folder.

In your own file, you'll have to define:
- Your custom functions. Be careful, your functions always have in inputs a dataset and a tag
- A dictionary which map your functions to a tag

## Anonymize dicom tags for a dataset

You can also anonymize dicom fields in-place for pydicom's DataSet using `anonymize_dataset`. See this example:
```python
import pydicom

from dicomanonymizer import anonymize_dataset

def main():

    # Create a list of tags object that should contains id, type and value
    fields = [
        { # Replaced by Anonymized
        'id': (0x0040, 0xA123),
        'type': 'LO',
        'value': 'Annie de la Fontaine',
        },
        { # Replaced with empty value
        'id': (0x0008, 0x0050),
        'type': 'TM',
        'value': 'bar',
        },
        { # Deleted
        'id': (0x0018, 0x4000),
        'type': 'VR',
        'value': 'foo',
        }
    ]

    # Create a readable dataset for pydicom
    data = pydicom.Dataset()

    # Add each field into the dataset
    for field in fields:
        data.add_new(field['id'], field['type'], field['value'])

    anonymize_dataset(data)

if __name__ == "__main__":
    main()
```

See the full application in the `examples` folder.

For more information about the pydicom's Dataset, please refer [here](https://pydicom.github.io/pydicom/stable/reference/generated/pydicom.dataset.Dataset.html).

You can also add `extra_anonymization_rules` as above:
```python
    anonymize_dataset(data_ds, extra_anonymization_rules, delete_private_tags=True)
```

# Actions list

| Action | Action definition |
| --- | --- |
| empty | Replace with a zero length value, or a non-zero length value that may be a dummy value and consistent with the VR** |
| delete | Completely remove the tag |
| keep | Do nothing on the tag |
| replace_UID | Replace all UID's number with a random one in order to keep consistent. Same UID will have the same replaced value |
| empty_or_replace | Replace with a non-zero length value that may be a dummy value and consistent with the VR** |
| delete_or_empty | Replace with a zero length value, or a non-zero length value that may be a dummy value and consistent with the VR** |
| delete_or_replace | Replace with a non-zero length value that may be a dummy value and consistent with the VR** |
| deleteOrEmptyOrReplace | Replace with a non-zero length value that may be a dummy value and consistent with the VR** |
| delete_or_empty_or_replace_UID | If it's a UID, then all numbers are randomly replaced. Else, replace with a zero length value, or a non-zero length value that may be a dummy value and consistent with the VR** |
|regexp| Find a value in the tag using a regexp and replace it with an arbitrary value. See the examples in this file to learn how to use.|
|replace_with_value| Replace the tag value with an arbitrary value. See the examples in this file to learn how to use.


** VR: Value Representation

Work originally done by Edern Haumont

# Change the DICOM anonymization standard

You can customize the DICOM standard that will be used to anonymize the dataset by giving an argument `base_rules_gen` to the function `anonymize_dicom_file` or `anonymize_dataset`.  
The value should be a function returning a dict of anonymization rules. Use the function `initialize_actions` to create such dict from a anonymization database from the folder `dicomanonymizer/dicom_anonymization_databases`.

Example:
```python
from dicomanonymizer.simpledicomanonymizer import anonymize_dataset, initialize_actions

anonymize_dataset(
    dataset, base_rules_gen=lambda: initialize_actions("dicomfields_2024b")
)
```