# DicomAnonymizer

Python package to anonymize DICOM files.
The anonymization answer to the standard . More information about dicom fields for anonymization can be found [here](https://dicom.nema.org/medical/dicom/current/output/html/part15.html#table_E.1-1).

The default behaviour of this package is to anonymize DICOM fields referenced in the 2023e DICOM standard. These fields are referenced in [dicomfields](dicomanonymizer/dicom_anonymization_databases/dicomfields_2023.py).  
Another standard can be selected, see *Change the DICOM anonymization standard*. 

Dicom fields are separated into different groups. Each groups will be anonymized in a different way.

| Group | Action | Action definition |
| --- | --- | --- |
| D_TAGS | replace | Replace with a non-zero length value that may be a dummy value and consistent with the VR** |
| Z_TAGS | empty | Replace with a zero length value, or a non-zero length value that may be a dummy value and consistent with the VR** |
| X_TAGS | delete | Completely remove the tag |
| U_TAGS | replace_UID | Replace all UID's random ones. Same UID will have the same replaced value |
| Z_D_TAGS | empty_or_replace | Replace with a non-zero length value that may be a dummy value and consistent with the VR** |
| X_Z_TAGS | delete_or_empty | Replace with a zero length value, or a non-zero length value that may be a dummy value and consistent with the VR** |
| X_D_TAGS | delete_or_replace | Replace with a non-zero length value that may be a dummy value and consistent with the VR** |
| X_Z_D_TAGS | delete_or_empty_or_replace | Replace with a non-zero length value that may be a dummy value and consistent with the VR** |
| X_Z_U_STAR_TAGS | delete_or_empty_or_replace_UID | If it's a UID, then all numbers are randomly replaced. Else, replace with a zero length value, or a non-zero length value that may be a dummy value and consistent with the VR**|
| ALL_TAGS | | Contains all previous defined tags

## Quirks

`dicom-anonymizer` is designed to retain date information within DICOM files, and will anonymize them rather than removing them entirely. This approach is taken to prevent potential crashes in certain applications that rely on these dates to work. This behavior complies with the DICOM standard, as mentioned in section [E.3.6](https://dicom.nema.org/medical/dicom/current/output/html/part15.html#sect_E.3.6).

## Documentation

 - [Installation](./doc/Setup_build_test.md)
 - [Usage](./doc/Usage)

## State of the library

No new features will be implemented by us unless we need them or we get financing.  
We will fix bugs that affect the use of the project.
All merge requests from the community will be considered, feel free to [open an issue](https://github.com/KitwareMedical/dicom-anonymizer/issues?q=is%3Aissue%20state%3Aopen%20label%3Aenhancement) to suggest new features.

## Financing

If you want a new feature in dicom-anonymizer or help manipulating DICOM files, feel free to reach out to us at contact@kitware.fr.