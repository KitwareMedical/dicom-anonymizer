from pydicom import dcmread
from pydicom.data import get_testdata_file
from dicomanonymizer import anonymize_dataset

def test_pydicom_data():

    sample_data = get_testdata_file("CT_small.dcm")
    ds = dcmread(sample_data)

    anonymize_dataset(ds)