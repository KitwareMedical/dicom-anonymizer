import argparse

from dicomanonymizer.dicomfields import ALL_TAGS
from dicomanonymizer import anonymize, keep


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

    input_dicom_path = args.input
    output_dicom_path = args.output

    extra_anonymization_rules = {}

    # Per https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html
    # it is all right to retain only the year part of the birth date for
    # de-identification purposes.
    def set_date_to_year(dataset, tag):
        element = dataset.get(tag)
        if element is not None:
            element.value = f"{element.value[:4]}0101"  # YYYYMMDD format

    # ALL_TAGS variable is defined on file dicomfields.py
    # the 'keep' method is already defined into the dicom-anonymizer
    # It will overrides the default behaviour
    for i in ALL_TAGS:
        extra_anonymization_rules[i] = keep

    extra_anonymization_rules[(0x0010, 0x0030)] = set_date_to_year  # Patient's Birth Date

    # Launch the anonymization
    anonymize(
        input_dicom_path,
        output_dicom_path,
        extra_anonymization_rules,
        delete_private_tags=False,
    )


if __name__ == "__main__":
    main()
