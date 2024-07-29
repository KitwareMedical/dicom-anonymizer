import pytest
import warnings

from pathlib import Path
from functools import lru_cache
from pydicom import dcmread
from pydicom.config import settings, IGNORE
from pydicom.data import get_testdata_files

from dicomanonymizer.simpledicomanonymizer import anonymize_dataset
from dicomanonymizer.dicom_anonymization_databases import dicomfields_2023

# Ignore warnings from pydicom validation
settings.writing_validation_mode = IGNORE
settings.reading_validation_mode = IGNORE

warnings.filterwarnings("ignore")


def get_all_failed():  # sourcery skip: inline-immediately-returned-variable
    # The following files are intended to fail dcmread
    # No point including them for anonymization testing
    dcmread_failed = [
        "ExplVR_BigEndNoMeta.dcm",
        "ExplVR_LitEndNoMeta.dcm",
        "no_meta.dcm",
        "rtstruct.dcm",
        "OT-PAL-8-face.dcm",
    ]

    return dcmread_failed


@lru_cache(maxsize=None)
def get_passing_files():
    all_files = get_testdata_files("*.dcm")
    all_failed = get_all_failed()
    return [x for x in all_files if Path(x).name not in all_failed]


@pytest.fixture(scope="module", params=get_passing_files())
def orig_anon_dataset(request):
    orig_ds = dcmread(request.param)
    orig_ds.filename = (
        None  # Non-None value causes warnings in copy(). Not needed for this testing
    )
    anon_ds = orig_ds.copy()
    anonymize_dataset(anon_ds)
    return (orig_ds, anon_ds)


def test_deleted_tags_are_removed(orig_anon_dataset):
    orig_ds, anon_ds = orig_anon_dataset
    deleted_tags = dicomfields_2023.X_TAGS

    for tt in deleted_tags:  # sourcery skip: no-loop-in-tests
        if (
            len(tt) == 2 and tt in orig_ds
        ):  # sourcery skip: merge-nested-ifs, no-conditionals-in-tests
            # TODO: Investigate why Date type are replaced instead of deleted
            # See issue https://github.com/KitwareMedical/dicom-anonymizer/issues/56
            if orig_ds[tt].VR != "DA":  # sourcery skip: no-conditionals-in-tests
                assert (
                    tt not in anon_ds
                ), f"({tt[0]:04X},{tt[1]:04x}):{orig_ds[tt].value}->{anon_ds[tt].value}"


changed_tags = (
    dicomfields_2023.U_TAGS
    + dicomfields_2023.D_TAGS
    + dicomfields_2023.Z_D_TAGS
    + dicomfields_2023.X_D_TAGS
    + dicomfields_2023.X_Z_D_TAGS
    + dicomfields_2023.X_Z_U_STAR_TAGS
)

empty_values = (0, "", "00010101", "000000.00", "ANONYMIZED")


def is_elem_replaced(orig, anon) -> bool:
    if orig.VR == "SQ":
        for x, y in zip(orig.value, anon.value):
            for tt in changed_tags:
                if tt in x and len(x[tt].value) > 0:
                    assert tt in y, f"({tt[0]:04X},{tt[1]:04x}):{x[tt].value}->missing!"
                    assert is_elem_replaced(
                        x[tt], y[tt]
                    ), f"({tt[0]:04X},{tt[1]:04x}):{x[tt].value} not replaced"
        return True

    return orig.value != anon.value if orig.value not in empty_values else True


def test_changed_tags_are_replaced(orig_anon_dataset):
    orig_ds, anon_ds = orig_anon_dataset

    for tt in changed_tags:  # sourcery skip: no-loop-in-tests
        if tt in orig_ds:  # sourcery skip: no-conditionals-in-tests
            assert (
                tt in anon_ds
            ), f"({tt[0]:04X},{tt[1]:04x}):{orig_ds[tt].value}->missing!"
            assert is_elem_replaced(
                orig_ds[tt], anon_ds[tt]
            ), f"({tt[0]:04X},{tt[1]:04x}):{orig_ds[tt].value} not replaced"


empty_tags = dicomfields_2023.Z_TAGS + dicomfields_2023.X_Z_TAGS


def is_elem_empty(elem) -> bool:
    if elem.VR == "SQ":
        for x in elem.value:
            for tt in empty_tags:
                if tt in x and len(x[tt].value) > 0:
                    assert is_elem_empty(
                        x[tt]
                    ), f"({tt[0]:04X},{tt[1]:04x}):{x[tt].value} is not empty"
        return True

    return elem.value in empty_values


def test_empty_tags_are_emptied(orig_anon_dataset):
    orig_ds, anon_ds = orig_anon_dataset

    for tt in empty_tags:  # sourcery skip: no-loop-in-tests
        if (
            tt in orig_ds and len(orig_ds[tt].value) > 0
        ):  # sourcery skip: no-conditionals-in-tests
            assert is_elem_empty(
                anon_ds[tt]
            ), f"({tt[0]:04X},{tt[1]:04x}):{anon_ds[tt].value} is not empty"
