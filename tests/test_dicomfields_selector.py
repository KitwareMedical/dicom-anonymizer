from dicomanonymizer.dicomfields_selector import selector

from dicomanonymizer import dicomfields, dicomfields_2024b


def test_selector():
    assert selector("2013") == {
        "D_TAGS": dicomfields.D_TAGS,
        "Z_TAGS": dicomfields.Z_TAGS,
        "X_TAGS": dicomfields.X_TAGS,
        "U_TAGS": dicomfields.U_TAGS,
        "Z_D_TAGS": dicomfields.Z_D_TAGS,
        "X_Z_TAGS": dicomfields.X_Z_TAGS,
        "X_D_TAGS": dicomfields.X_D_TAGS,
        "X_Z_D_TAGS": dicomfields.X_Z_D_TAGS,
        "X_Z_U_STAR_TAGS": dicomfields.X_Z_U_STAR_TAGS,
        "ALL_TAGS": dicomfields.ALL_TAGS,
    }
    assert selector("2024b") == {
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

    assert selector() == selector("2013")

    try:
        selector("2019")
    except ValueError as e:
        assert str(e) == "Unknown DICOM version: 2019"
    else:
        assert False
