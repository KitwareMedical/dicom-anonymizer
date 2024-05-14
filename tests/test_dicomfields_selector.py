from dicomanonymizer.dicom_anonymization_databases import dicomfields_2024b
from dicomanonymizer.dicomfields_selector import dicom_anonymization_database_selector

from dicomanonymizer.dicom_anonymization_databases import dicomfields_2013


def test_selector():
    assert dicom_anonymization_database_selector("dicomfields_2013") == {
        "D_TAGS": dicomfields_2013.D_TAGS,
        "Z_TAGS": dicomfields_2013.Z_TAGS,
        "X_TAGS": dicomfields_2013.X_TAGS,
        "U_TAGS": dicomfields_2013.U_TAGS,
        "Z_D_TAGS": dicomfields_2013.Z_D_TAGS,
        "X_Z_TAGS": dicomfields_2013.X_Z_TAGS,
        "X_D_TAGS": dicomfields_2013.X_D_TAGS,
        "X_Z_D_TAGS": dicomfields_2013.X_Z_D_TAGS,
        "X_Z_U_STAR_TAGS": dicomfields_2013.X_Z_U_STAR_TAGS,
        "ALL_TAGS": dicomfields_2013.ALL_TAGS,
    }
    assert dicom_anonymization_database_selector("dicomfields_2024b") == {
        "D_TAGS": dicomfields_2024b.D_TAGS,
        "Z_TAGS": dicomfields_2024b.Z_TAGS,
        "X_TAGS": dicomfields_2024b.X_TAGS,
        "U_TAGS": dicomfields_2024b.U_TAGS,
        "Z_D_TAGS": dicomfields_2024b.Z_D_TAGS,
        "X_Z_TAGS": dicomfields_2024b.X_Z_TAGS,
        "X_D_TAGS": dicomfields_2024b.X_D_TAGS,
        "X_Z_D_TAGS": dicomfields_2024b.X_Z_D_TAGS,
        "X_Z_U_STAR_TAGS": dicomfields_2024b.X_Z_U_STAR_TAGS,
        "ALL_TAGS": dicomfields_2024b.ALL_TAGS,
    }

    # check default selector
    assert (
        dicom_anonymization_database_selector()
        == dicom_anonymization_database_selector("dicomfields_2013")
    )

    try:
        dicom_anonymization_database_selector("2019")
    except ValueError as e:
        assert str(e) == "Unknown DICOM anonymization database: 2019"
    else:
        assert False
