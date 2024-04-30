import pydicom

from dicomanonymizer import anonymize_dataset
from dicomanonymizer.simpledicomanonymizer import empty


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
