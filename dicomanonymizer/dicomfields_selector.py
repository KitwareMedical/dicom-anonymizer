from dicomanonymizer import dicomfields, dicomfields_2024b


def selector(dicom_version: str = "2013") -> dict:
    if dicom_version == "2013":
        return {
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
    elif dicom_version == "2024b":
        return {
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
    else:
        raise ValueError(f"Unknown DICOM version: {dicom_version}")
