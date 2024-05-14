import importlib

ANONYMIZATION_CATEGORIES = [
    "D_TAGS",
    "Z_TAGS",
    "X_TAGS",
    "U_TAGS",
    "Z_D_TAGS",
    "X_Z_TAGS",
    "X_D_TAGS",
    "X_Z_D_TAGS",
    "X_Z_U_STAR_TAGS",
    "ALL_TAGS",
]


def dicom_anonymization_database_selector(
    dicom_version: str = "dicomfields_2013",
) -> dict:
    try:
        dicom_anonymization_database = importlib.import_module(
            f"dicomanonymizer.dicom_anonymization_databases.{dicom_version}"
        )
    except ModuleNotFoundError:
        raise ValueError(f"Unknown DICOM anonymization database: {dicom_version}")

    try:
        dicom_anonymization_dict = {
            anonymization_category: getattr(
                dicom_anonymization_database, anonymization_category
            )
            for anonymization_category in ANONYMIZATION_CATEGORIES
        }
    except AttributeError:
        print(
            f"Anonymization database {dicom_version} is missing a category, please check it has them all."
        )
        raise
    return dicom_anonymization_dict
