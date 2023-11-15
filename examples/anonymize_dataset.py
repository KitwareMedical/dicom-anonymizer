from dicomanonymizer import anonymize_dataset
from pydicom.data import get_testdata_file
from pydicom import dcmread

def main():
    original_ds = dcmread(get_testdata_file("CT_small.dcm"))
    data_ds = original_ds.copy()
    anonymize_dataset(data_ds) # Anonymization is done in-place
    print("Examples of original -> anonymized values:")
    for tt in ["PatientName", "PatientID", "StudyDate"]:
        print(f"  {tt}: '{original_ds[tt].value}' -> '{data_ds[tt].value}'")

if __name__ == "__main__":
    main()
