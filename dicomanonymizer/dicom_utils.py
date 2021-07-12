from typing import List
import pydicom
from pydicom.dataelem import RawDataElement


def exposure_callback(raw_data_element: RawDataElement, encoding: List[str]):
    if raw_data_element.tag == "Exposure":
        value = raw_data_element.value.decode(encoding[0])
        new_value = str(round(float(value)))
        new_value = new_value.encode(encoding[0])
        raw_data_element = raw_data_element._replace(value=new_value)
    return raw_data_element


def fix_exposure():
    pydicom.config.data_element_callback = exposure_callback