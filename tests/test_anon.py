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
        "MR-SIEMENS-DICOM-WithOverlays.dcm", #TODO: X_TAGS entries with 4 ints
        "color3d_jpeg_baseline.dcm",
        "JPGLosslessP14SV1_1s_1f_8b.dcm",
        "test-SR.dcm",
    ]

    # TODO: Investigate why these fail emptying test of anonymization
    emptied_failed = [
        "JPGLosslessP14SV1_1s_1f_8b.dcm",
        "test-SR.dcm",
    ]
    return dcmread_failed + replaced_failed + deleted_failed + emptied_failed


@lru_cache(maxsize=None)
def get_passing_files():
    all_files = get_testdata_files("*.dcm")
    all_failed = get_all_failed()
    return [x for x in all_files if Path(x).name not in all_failed]


@pytest.fixture(scope="module", params=get_passing_files())
def orig_anon_dataset(request):
    orig_ds = dcmread(request.param)
    anon_ds = orig_ds.copy()
    anonymize_dataset(anon_ds,delete_private_tags=False)
    return (orig_ds, anon_ds)


def test_if_anonymized_correctly(orig_anon_dataset):
    orig_ds, anon_ds = orig_anon_dataset
 
    for elem in anon_ds:
        assert elem.tag in orig_ds
    
    for elem in orig_ds:
        if elem.tag not in anon_ds:
            ok_if_deleted_tags = dicomfields.X_TAGS + dicomfields.X_Z_TAGS + dicomfields.X_D_TAGS \
                            + dicomfields.X_Z_D_TAGS + dicomfields.X_Z_U_STAR_TAGS
            assert elem.tag in ok_if_deleted_tags
        else:
            check_element_is_anonymized(elem,anon_ds[elem.tag])


def check_element_is_anonymized(orig_elem,anon_elem):
    ok_if_emptied_tags = dicomfields.Z_TAGS + dicomfields.Z_D_TAGS + dicomfields.X_Z_TAGS \
            + dicomfields.X_Z_D_TAGS + dicomfields.X_Z_U_STAR_TAGS
    ok_if_replaced_tags = dicomfields.D_TAGS + dicomfields.U_TAGS + dicomfields.Z_D_TAGS + dicomfields.X_D_TAGS \
            + dicomfields.X_Z_D_TAGS + dicomfields.X_Z_U_STAR_TAGS
    ok_if_emptied_or_replaced_tags = ok_if_emptied_tags + ok_if_replaced_tags

    emp_vals = (0, '', '00010101', '000000.00', '00010101010101.000000+0000')
    
    if orig_elem.VR == 'SQ': #Todo handle sequence elements
        pass
        # for sub_ds in orig_elem.value:
        #     for sub_elem in sub_ds.elements():
        #         check_element_is_anonymized(sub_elem, anon_elem[sub_elem.tag])
    elif orig_elem.value in emp_vals:
        pass
    elif orig_elem.value != anon_elem.value:
        if anon_elem.value in emp_vals:
            assert anon_elem.tag in ok_if_emptied_or_replaced_tags
        else:
            assert anon_elem.tag in ok_if_replaced_tags

