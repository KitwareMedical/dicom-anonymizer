from typing import List
import pydicom
from pydicom.dataelem import RawDataElement


def exposure_callback(raw_data_element: RawDataElement, encoding: List[str]):
    """Workaround for known pydicom issue insisting on dicom-compliant
    types. Exposure should be Integer String type. In case it is float,
    dicom breaks fast then you access the field. So, round it here.
    Hacky way, I don't like it.

    Args:
        raw_data_element (RawDataElement): provided by the main lib routine
        encoding (List[str]): same here

    Returns:
        [type]: raw_data_element with updated exposure value
    """
    if raw_data_element.tag == "Exposure":
        value = raw_data_element.value.decode(encoding[0])
        try:
            new_value = str(round(float(value)))
        except ValueError:
            new_value = value.split(",")[0]
        new_value = new_value.encode(encoding[0])
        raw_data_element = raw_data_element._replace(value=new_value)
    return raw_data_element


def fix_exposure():
    pydicom.config.data_element_callback = exposure_callback
