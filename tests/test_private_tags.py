import pydicom
import pytest

from dicomanonymizer import anonymize_dataset, delete, keep, replace


@pytest.fixture(name="ds")
def ds_with_one_private_creator():
    # Create a readable dataset for pydicom
    ds = pydicom.Dataset()
    ds.AccessionNumber = 123456  # to be zero
    ds.PatientName = "Test^Name"  # to be removed

    private_block = ds.private_block(0x0019, "Private Creator", create=True)
    # Add new private tags
    private_block.add_new(0x01, "LT", "Test value 1")
    private_block.add_new(0x02, "LT", "Test value 2")

    return ds


@pytest.fixture(name="ds2")
def ds_with_two_private_creators():
    # Create a readable dataset for pydicom
    ds = pydicom.Dataset()
    ds.AccessionNumber = "123456"  # to be emptied.
    ds.PatientName = "Test^Name"  # to be emptied.

    private_block = ds.private_block(0x0019, "Private Creator1", create=True)
    # Add new private tags
    private_block.add_new(0x01, "LT", "Test value 11")
    private_block.add_new(0x02, "LT", "Test value 12")

    private_block2 = ds.private_block(0x0021, "Private Creator2", create=True)
    # Add new private tags
    private_block2.add_new(0x01, "LT", "Test value 21")
    private_block2.add_new(0x02, "LT", "Test value 22")
    private_block2.add_new(0x03, "LT", "Test value 23")

    return ds


def test_donot_delete_private_tags(ds):
    anonymize_dataset(ds, delete_private_tags=False)

    # to confirm the basic anonymization
    assert ds.AccessionNumber == ""
    assert ds.PatientName == ""

    # private tags should not be removed.
    assert ds[(0x0019, 0x0010)].value == "Private Creator"
    assert ds[(0x0019, 0x1001)].value == "Test value 1"
    assert ds[(0x0019, 0x1002)].value == "Test value 2"


def test_delete_private_tags(ds):
    anonymize_dataset(ds)

    # to confirm the basic anonymization
    assert ds.AccessionNumber == ""
    assert ds.PatientName == ""

    # by default, private tags are removed.
    assert (0x0019, 0x0010) not in ds  # Private Creator
    assert (0x0019, 0x1001) not in ds  # Test value 1
    assert (0x0019, 0x1001) not in ds  # Test value 2


def test_keep_prviate_tags_by_extra_rules(ds2):
    # keep values from Private Creator 2
    extra_rules = {
        (0x0021, 0x0001, 0xFFFF, 0x00FF): delete,
        (0x0021, 0x0002, 0xFFFF, 0x00FF): replace,
        (0x0021, 0x0003, 0xFFFF, 0x00FF): keep,
    }

    anonymize_dataset(ds2, extra_anonymization_rules=extra_rules, delete_private_tags=True)

    assert ds2.AccessionNumber == ""
    assert ds2.PatientName == ""
    assert (0x0019, 0x0010) not in ds2  # Private Creator
    assert (0x0019, 0x1001) not in ds2  # Test value 1
    assert (0x0019, 0x1001) not in ds2  # Test value2

    # Offset for Private Creator now becomes 0x10 from 0x11, since Private Creator 1 is removed.
    assert ds2[(0x0021, 0x0010)].value == "Private Creator2"
    assert (0x0021, 0x1001) not in ds2
    assert ds2[(0x0021, 0x1002)].value == "ANONYMIZED"
    assert ds2[(0x0021, 0x1003)].value == "Test value 23"
