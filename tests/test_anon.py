from pydicom import dcmread
from pydicom import tag
from pydicom.data import get_testdata_file
from dicomanonymizer import dicomfields
from dicomanonymizer import anonymize_dataset


def test_pydicom_data():
    sample_data = get_testdata_file("CT_small.dcm")
    ds = dcmread(sample_data)
    original_ds = ds.copy()

    #  for tt in dicomfields.Z_TAGS:
    #     if tt in original_ds:
    #         assert tt in [0, "", None]

    anonymize_dataset(ds)

    for tt in dicomfields.X_TAGS:
        if len(tt) == 2 and tt in original_ds:
            assert tt not in ds

    for tt in dicomfields.U_TAGS:
        if tt in original_ds:
            assert ds[tt] != original_ds[tt]

    for tt in dicomfields.D_TAGS:
        if tt in original_ds:
            assert ds[tt] != original_ds[tt]

    for tt in dicomfields.Z_TAGS:
        if tt in original_ds:
            assert ds[tt].value in (0, "", "00010101", "000000.00")
