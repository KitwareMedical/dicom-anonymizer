from pydicom import dcmread
from pydicom.data import get_testdata_file
from dicomanonymizer import dicomfields
from dicomanonymizer import anonymize_dataset


def test_pydicom_data():
    sample_data = get_testdata_file("CT_small.dcm")
    ds = dcmread(sample_data)
    original_ds = ds.copy()

    anonymize_dataset(ds)

    verify_anonmyzation(original_ds, ds)


def verify_anonmyzation(orig_ds, anon_ds):
    verify_deleted_tags(orig_ds, anon_ds)
    verify_changed_tags(orig_ds, anon_ds)
    verify_empty_tags(orig_ds, anon_ds)


def verify_deleted_tags(orig_ds, anon_ds):
    deleted_tags = dicomfields.X_TAGS

    for tt in deleted_tags:
        if len(tt) == 2 and tt in orig_ds:
            assert tt not in anon_ds


def verify_changed_tags(orig_ds, anon_ds):
    changed_tags = []
    changed_tags.extend(dicomfields.U_TAGS)
    changed_tags.extend(dicomfields.D_TAGS)
    changed_tags.extend(dicomfields.Z_D_TAGS)
    changed_tags.extend(dicomfields.X_D_TAGS)
    changed_tags.extend(dicomfields.X_Z_D_TAGS)
    changed_tags.extend(dicomfields.X_Z_U_STAR_TAGS)

    for tt in changed_tags:
        if tt in orig_ds:
            assert anon_ds[tt] != orig_ds[tt]


def verify_empty_tags(orig_ds, anon_ds):
    empty_values = (0, "", "00010101", "000000.00")
    empty_tags = []
    empty_tags.extend(dicomfields.Z_TAGS)
    empty_tags.extend(dicomfields.X_Z_TAGS)

    for tt in empty_tags:
        if tt in orig_ds:
            assert anon_ds[tt].value in empty_values
