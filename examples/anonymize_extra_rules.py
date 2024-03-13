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
    parser.add_argument(
        "--suffix",
        action="store",
        help="Suffix that will be added at the end of series description",
    )
    args = parser.parse_args()

    input_dicom_path = args.input
    output_dicom_path = args.output

    extra_anonymization_rules = {}

    def setup_series_description(dataset, tag):
        element = dataset.get(tag)
        if element is not None:
            element.value = f"{element.value}-{args.suffix}"

    # ALL_TAGS variable is defined on file dicomfields.py
    # the 'keep' method is already defined into the dicom-anonymizer
    # It will overrides the default behaviour
    for i in ALL_TAGS:
        extra_anonymization_rules[i] = keep

    if args.suffix:
        extra_anonymization_rules[(0x0008, 0x103E)] = setup_series_description

    # Launch the anonymization
    anonymize(
        input_dicom_path,
        output_dicom_path,
        extra_anonymization_rules,
        delete_private_tags=False,
    )


if __name__ == "__main__":
    main()
