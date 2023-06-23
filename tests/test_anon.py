from pydicom import dcmread
from pydicom import tag
from pydicom.data import get_testdata_file
from dicomanonymizer import dicomfields
from dicomanonymizer import anonymize_dataset


def test_pydicom_data():
    sample_data = get_testdata_file("CT_small.dcm")
    ds = dcmread(sample_data)
    original_ds = ds.copy()

    anonymize_dataset(ds)

    for tt in dicomfields.X_TAGS:
        if len(tt) == 2 and tt in original_ds:
            assert tt not in ds
