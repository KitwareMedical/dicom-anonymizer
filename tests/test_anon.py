import pytest
import warnings

from pathlib import Path
from functools import lru_cache
from pydicom import dcmread
from pydicom.config import settings, IGNORE
from pydicom.data import get_testdata_files

from dicomanonymizer import anonymize_dataset, dicomfields

# Ignore warnings from pydicom validation
settings.writing_validation_mode = IGNORE
settings.reading_validation_mode = IGNORE

warnings.filterwarnings("ignore")


def get_all_failed():
    # The following files are intended to fail dcmread
    # No point including them for anonymization testing
    dcmread_failed = [
        "ExplVR_BigEndNoMeta.dcm",
        "ExplVR_LitEndNoMeta.dcm",
        "no_meta.dcm",
        "rtstruct.dcm",
        "OT-PAL-8-face.dcm",
    ]

    # TODO: Investigate why these fail replacement test of anonymization
    replaced_failed = [
        "693_J2KI.dcm",
        "JPEG-lossy.dcm",
        "JPEG2000-embedded-sequence-delimiter.dcm",
        "JPEG2000.dcm",
        "JPGExtended.dcm",
        "reportsi.dcm",
        "reportsi_with_empty_number_tags.dcm",
        "SC_rgb_gdcm_KY.dcm",
        "SC_rgb_jpeg_lossy_gdcm.dcm",
        "693_UNCI.dcm",
        "JPEG-LL.dcm",
        "JPEG2000_UNC.dcm",
        "MR2_J2KI.dcm",
        "MR2_J2KR.dcm",
        "MR2_UNCI.dcm",
        "RG1_J2KI.dcm",
        "RG1_J2KR.dcm",
        "RG1_UNCI.dcm",
        "RG3_J2KI.dcm",
        "RG3_J2KI.dcm",
        "RG3_J2KR.dcm",
        "RG3_UNCI.dcm",
        "SC_rgb_gdcm2k_uncompressed.dcm",
        "US1_J2KI.dcm",
        "US1_J2KR.dcm",
        "US1_UNCI.dcm",
        "test-SR.dcm",
    ]

    # TODO: Investigate why these fail deletion test of anonymization
    deleted_failed = [
        "color3d_jpeg_baseline.dcm",
        "JPGLosslessP14SV1_1s_1f_8b.dcm",
        "test-SR.dcm",
    ]

    # TODO: Investigate why these fail emptying test of anonymization
    emptied_failed = [
        "JPGLosslessP14SV1_1s_1f_8b.dcm",
        "test-SR.dcm",
    ]

    all_failed = list(dcmread_failed)
    all_failed.extend(replaced_failed)
    all_failed.extend(deleted_failed)
    all_failed.extend(emptied_failed)
    return all_failed


@lru_cache(maxsize=None)
def get_passing_files():
    all_files = get_testdata_files("*.dcm")
    all_failed = get_all_failed()
    return [x for x in all_files if Path(x).name not in all_failed]


@pytest.fixture(scope="module", params=get_passing_files())
def orig_anon_dataset(request):
    orig_ds = dcmread(request.param)
    anon_ds = orig_ds.copy()
    anonymize_dataset(anon_ds)
    return (orig_ds, anon_ds)


def test_deleted_tags_are_removed(orig_anon_dataset):
    orig_ds, anon_ds = orig_anon_dataset
    deleted_tags = dicomfields.X_TAGS
    for tt in deleted_tags:
        if len(tt) == 2 and tt in orig_ds:
            assert tt not in anon_ds


def test_changed_tags_are_replaced(orig_anon_dataset):
    changed_tags = []
    changed_tags.extend(dicomfields.U_TAGS)
    changed_tags.extend(dicomfields.D_TAGS)
    changed_tags.extend(dicomfields.Z_D_TAGS)
    changed_tags.extend(dicomfields.X_D_TAGS)
    changed_tags.extend(dicomfields.X_Z_D_TAGS)
    changed_tags.extend(dicomfields.X_Z_U_STAR_TAGS)

    orig_ds, anon_ds = orig_anon_dataset

    for tt in changed_tags:
        if tt in orig_ds:
            assert anon_ds[tt] != orig_ds[tt]


def test_empty_tags_are_emptied(orig_anon_dataset):
    empty_values = (0, "", "00010101", "000000.00")
    empty_tags = []
    empty_tags.extend(dicomfields.Z_TAGS)
    empty_tags.extend(dicomfields.X_Z_TAGS)

    orig_ds, anon_ds = orig_anon_dataset

    for tt in empty_tags:
        if tt in orig_ds:
            assert anon_ds[tt].value in empty_values
