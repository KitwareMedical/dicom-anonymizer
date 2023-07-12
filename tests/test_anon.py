from pydicom.data import get_testdata_file
import pytest
from dicomanonymizer import dicomfields
from dicomanonymizer import anonymize_dataset


@pytest.fixture(scope="module")
def CT_small_anonymized_dataset():
    orig_ds = get_testdata_file("CT_small.dcm", read=True)
    anon_ds = orig_ds.copy()
    anonymize_dataset(anon_ds)
    return (orig_ds, anon_ds)


def test_deleted_tags_are_removed(CT_small_anonymized_dataset):
    orig_ds, anon_ds = CT_small_anonymized_dataset
    deleted_tags = dicomfields.X_TAGS
    for tt in deleted_tags:
        if len(tt) == 2 and tt in orig_ds:
            assert tt not in anon_ds


def test_changed_tags_are_replaced(CT_small_anonymized_dataset):
    changed_tags = []
    changed_tags.extend(dicomfields.U_TAGS)
    changed_tags.extend(dicomfields.D_TAGS)
    changed_tags.extend(dicomfields.Z_D_TAGS)
    changed_tags.extend(dicomfields.X_D_TAGS)
    changed_tags.extend(dicomfields.X_Z_D_TAGS)
    changed_tags.extend(dicomfields.X_Z_U_STAR_TAGS)

    orig_ds, anon_ds = CT_small_anonymized_dataset

    for tt in changed_tags:
        if tt in orig_ds:
            assert anon_ds[tt] != orig_ds[tt]


def test_empty_tags_are_emptied(CT_small_anonymized_dataset):
    empty_values = (0, "", "00010101", "000000.00")
    empty_tags = []
    empty_tags.extend(dicomfields.Z_TAGS)
    empty_tags.extend(dicomfields.X_Z_TAGS)

    orig_ds, anon_ds = CT_small_anonymized_dataset

    for tt in empty_tags:
        if tt in orig_ds:
            assert anon_ds[tt].value in empty_values
