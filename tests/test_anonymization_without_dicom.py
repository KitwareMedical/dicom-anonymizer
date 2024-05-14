import pydicom

from dicomanonymizer import anonymize_dataset
from dicomanonymizer.simpledicomanonymizer import (
    empty,
    initialize_actions,
    initialize_actions_2024b,
)


def test_anonymization_without_dicom_file():
    # Create a list of tags object that should contains id, type and value
    fields = [
        {  # Replaced by Anonymized
            "id": (0x0040, 0xA123),
            "type": "LO",
            "value": "Annie de la Fontaine",
        },
        {  # Replaced with empty value
            "id": (0x0008, 0x0050),
            "type": "TM",
            "value": "bar",
        },
        {  # Deleted
            "id": (0x0018, 0x4000),
            "type": "VR",
            "value": "foo",
        },
        {  # Relaced with empty value via extra anonymization rules since no tags with IS value type are anonymized by default.
            "id": (0x0020, 0x0012),
            "type": "IS",
            "value": "123",
        },
    ]

    # Create a readable dataset for pydicom
    data = pydicom.Dataset()

    # Add each field into the dataset
    for field in fields:  # sourcery skip: no-loop-in-tests
        data.add_new(field["id"], field["type"], field["value"])

    anonymize_dataset(data, extra_anonymization_rules={(0x0020, 0x0012): empty})

    assert data[(0x0040, 0xA123)].value == "ANONYMIZED"
    assert data[(0x0008, 0x0050)].value == "000000.00"
    assert (0x0018, 0x4000) not in data
    assert int(data[(0x0020, 0x0012)].value) == 0


def test_anonymization_of_ranged_tags_without_dicom_file():
    """Test the anonymization of ranged tags in a dataset without a DICOM file."""
    # Create Curve Data (50xx, xxxx) which must be deleted
    # per (0x5000, 0x0000, 0xFF00, 0x0000) rule.
    fields = [
        {  # to be deleted
            "id": (0x5011, 0x0110),  # Curve Data Descriptor
            "type": "US",
            "value": "dummy curve data descriptor 1",
        },
        {  # to be deleted
            "id": (0x5012, 0x0112),  # Coordinate Start Value
            "type": "US",
            "value": "dummy curve data descriptor 2",
        },
    ]

    # Create a readable dataset for pydicom
    data = pydicom.Dataset()

    # Add each field into the dataset
    for field in fields:  # sourcery skip: no-loop-in-tests
        data.add_new(field["id"], field["type"], field["value"])

    anon_ds = data.copy()
    anonymize_dataset(anon_ds)

    # Check that the dataset has been anonymized
    assert (0x5011, 0x0110) not in anon_ds
    assert (0x5012, 0x0112) not in anon_ds


def test_switching_dicom_versions():
    """To confirm the different behavior of annonymization beteen dicom versions of 2013 and 2024b.

    In 2013, anonymization method of Patient ID is marked as "Z" (empty value) while it becomes Z/D
    in 2024b.

    Note, VR of Patient ID remains LO in 2013 and 2024b ("current" is 2024b as of 2024.05.14).
    https://dicom.nema.org/dicom/2013/output/chtml/part06/chapter_6.html#table_6-1
    https://dicom.nema.org/dicom/current/output/chtml/part06/chapter_6.html#table_6-1
    """
    fields = [
        {  # Replaced by Anonymized
            "id": (0x0010, 0x0020),
            "type": "LO",
            "value": "Test Patient ID",
        },
    ]

    # Create a readable dataset for pydicom
    data = pydicom.Dataset()
    data_2013 = pydicom.Dataset()
    data_2024b = pydicom.Dataset()

    for field in fields:  # sourcery skip: no-loop-in-tests
        data.add_new(field["id"], field["type"], field["value"])
        data_2013.add_new(field["id"], field["type"], field["value"])
        data_2024b.add_new(field["id"], field["type"], field["value"])

    anonymize_dataset(data, base_rules_gen=initialize_actions)
    anonymize_dataset(
        data_2013, base_rules_gen=lambda: initialize_actions("dicomfields_2013")
    )
    anonymize_dataset(data_2024b, base_rules_gen=initialize_actions_2024b)

    assert data[(0x0010, 0x0020)].value == ""  # default behavior which is DICOM 2013.
    assert data_2013[(0x0010, 0x0020)].value == ""  # same as the default.
    assert (
        data_2024b[(0x0010, 0x0020)].value == "ANONYMIZED"
    )  # 2024b differs from the default
