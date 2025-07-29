import pydicom
import re

from enum import Enum
from typing import Callable, List, Union
from dataclasses import dataclass

from dicomanonymizer.dicomfields_selector import dicom_anonymization_database_selector
from dicomanonymizer.format_tag import tag_to_hex_strings

# keeps the mapping from old UID to new UID
dictionary = {}


# Regexp function


def regexp(options: Union[list, dict]):
    """
    Apply a regexp method to the dataset

    :param options: contains two values:
        - find: the regexp that will be used to find the string to replace
        - replace: string that will replace the regexp matches
    If options is a list, find is expected to be the first value.
    """

    def apply_regexp(dataset, tag):
        """
        Apply a regexp to the dataset
        """
        if isinstance(options, dict):
            try:
                find = options["find"]
                replace = options["replace"]
            except KeyError as e:
                raise ValueError(f"Missing field in tag dictionary {tag}: {e.args[0]}")
        else:
            find, replace = options

        element = dataset.get(tag)
        if element is not None:
            element.value = re.sub(find, replace, str(element.value))

    return apply_regexp


def replace_with_value(options: Union[list, dict]):
    """
    Replace the given tag with a predefined value.

    :param options: contains one value:
        - value: the string used to replace the tag value
    If options is a list, value is expected to be the first value.
    """

    def apply_replace_with_value(dataset, tag):
        if isinstance(options, dict):
            try:
                value = options["value"]
            except KeyError as e:
                raise ValueError(f"Missing field in tag dictionary {tag}: {e.args[0]}")
        else:
            value = options[0]

        element = dataset.get(tag)
        if element is not None:
            element.value = value

    return apply_replace_with_value


# Default anonymization functions


def get_UID(old_uid: str) -> str:
    """
    Lookup new UID in cached dictionary or create new one if none found
    """
    from pydicom.uid import generate_uid

    if old_uid not in dictionary:
        dictionary[old_uid] = generate_uid(None)
    return dictionary.get(old_uid)


def replace_element_UID(element):
    """
    Replace UID(s) with random UID(s)
    The replaced value is kept in a dictionary link to the initial element.value in order to automatically
    apply the same replaced value if we have an other UID with the same value
    """
    from pydicom.multival import MultiValue

    if isinstance(element.value, MultiValue):
        # Example of multi-value UID situation: IrradiationEventUID, (0008,3010)
        for k, v in enumerate(element.value):
            element.value[k] = get_UID(v)
    else:
        element.value = get_UID(element.value)


def replace_date_time_element(element):
    """
    Handle the anonymization of date and time related elements.

    Date and time elements are all handled in the same way, whether they are emptied or removed.
    """
    if element.VR == "DA":
        replace_element_date(element)
    elif element.VR == "DT":
        replace_element_date_time(element)
    elif element.VR == "TM":
        replace_element_time(element)


def replace_element_date(element):
    """
    Replace date element's value with '00010101'
    """
    element.value = "00010101"


def replace_element_date_time(element):
    """
    Replace date time element's value with '00010101010101.000000+0000'
    """
    element.value = "00010101010101.000000+0000"


def replace_element_time(element):
    """
    Replace time element's value with '000000.00'
    """
    element.value = "000000.00"


def replace_element(element):
    """
    Replace element's value according to it's VR:
    - LO, LT, SH, PN, CS, ST, UT: replace with 'Anonymized'
    - UI: cf replace_element_UID
    - DS and IS: value will be replaced by '0'
    - FD, FL, SS, US, SL, UL: value will be replaced by 0
    - DA: value will be replaced by '00010101'
    - DT: value will be replaced by '00010101010101.000000+0000'
    - TM: value will be replaced by '000000.00'
    - UN: value will be replaced by b'Anonymized' (binary string)
    - SQ: call replace_element for all sub elements

    See https://laurelbridge.com/pdf/Dicom-Anonymization-Conformance-Statement.pdf
    """
    if element.VR in ("LO", "LT", "SH", "PN", "CS", "ST", "UT"):
        element.value = "ANONYMIZED"  # CS VR accepts only uppercase characters
    elif element.VR == "UI":
        replace_element_UID(element)
    elif element.VR in ("DS", "IS"):
        element.value = "0"
    elif element.VR in ("FD", "FL", "SS", "US", "SL", "UL"):
        element.value = 0
    elif element.VR in ("DT", "DA", "TM"):
        replace_date_time_element(element)
    elif element.VR == "UN":
        element.value = b"Anonymized"
    elif element.VR == "SQ":
        for sub_dataset in element.value:
            for sub_element in sub_dataset.elements():
                if isinstance(sub_element, pydicom.dataelem.RawDataElement):
                    # RawDataElement is a NamedTuple, so cannot set its value attribute.
                    # Convert it to a DataElement, replace value, and set it back.
                    # Found in https://github.com/KitwareMedical/dicom-anonymizer/issues/63
                    e2 = pydicom.dataelem.DataElement_from_raw(sub_element)
                    replace_element(e2)
                    sub_dataset.add(e2)
                else:
                    replace_element(sub_element)
    else:
        raise NotImplementedError(
            "Not anonymized. VR {} not yet implemented.".format(element.VR)
        )


def replace(dataset, tag):
    """
    D - replace with a non-zero length value that may be a dummy value and consistent with the
    VR
    """
    element = dataset.get(tag)
    if element is not None:
        replace_element(element)


def empty_element(element):
    """
    Clean element according to the element's VR:
    - SH, PN, UI, LO, LT, CS, AS, ST and UT: value will be set to ''
    - DA: value will be replaced by '00010101'
    - DT: value will be replaced by '00010101010101.000000+0000'
    - TM: value will be replaced by '000000.00'
    - UL, FL, FD, SL, SS and US: value will be replaced by 0
    - DS and IS: value will be replaced by '0'
    - UN: value will be replaced by: b'' (binary string)
    - SQ: all subelement will be called with "empty_element"

    Date and time related VRs are not emptied by replacing their values with a empty string to keep
    the consistency with some software who expect a non null value for those VRs.

    See: https://laurelbridge.com/pdf/Dicom-Anonymization-Conformance-Statement.pdf
    """
    if element.VR in ("SH", "PN", "UI", "LO", "LT", "CS", "AS", "ST", "UT"):
        element.value = ""
    elif element.VR in ("DT", "DA", "TM"):
        replace_date_time_element(element)
    elif element.VR in ("UL", "FL", "FD", "SL", "SS", "US"):
        element.value = 0
    elif element.VR in ("DS", "IS"):
        element.value = "0"
    elif element.VR == "UN":
        element.value = b""
    elif element.VR == "SQ":
        for sub_dataset in element.value:
            for sub_element in sub_dataset.elements():
                empty_element(sub_element)
    else:
        raise NotImplementedError(
            "Not anonymized. VR {} not yet implemented.".format(element.VR)
        )


def empty(dataset, tag):
    """
    Z - replace with a zero length value, or a non-zero length value that may be a dummy value and
    consistent with the VR
    """
    element = dataset.get(tag)
    if element is not None:
        empty_element(element)


def delete_element(dataset, element):
    """
    Delete the element from the dataset.
    If VR's element is a date, then it will be replaced by 00010101
    """
    if element.VR == "DA":
        replace_element_date(element)
    elif element.VR == "SQ" and element.value is type(pydicom.Sequence):
        for sub_dataset in element.value:
            for sub_element in sub_dataset.elements():
                delete_element(sub_dataset, sub_element)
    else:
        del dataset[element.tag]


def delete(dataset, tag):
    """X - remove"""
    element = dataset.get(tag)
    if element is not None:
        delete_element(dataset, element)  # element.tag is not the same type as tag.


def keep(dataset, tag):
    """K - keep (unchanged for non-sequence attributes, cleaned for sequences)"""
    pass


def replace_UID(dataset, tag):
    """
    U - replace with a non-zero length UID that is internally consistent within a set of Instances
    Lazy solution : Replace with empty string
    """
    element = dataset.get(tag)
    if element is not None:
        replace_element_UID(element)


def empty_or_replace(dataset, tag):
    """Z/D - Z unless D is required to maintain IOD conformance (Type 2 versus Type 1)"""
    replace(dataset, tag)


def delete_or_empty(dataset, tag):
    """X/Z - X unless Z is required to maintain IOD conformance (Type 3 versus Type 2)"""
    empty(dataset, tag)


def delete_or_replace(dataset, tag):
    """X/D - X unless D is required to maintain IOD conformance (Type 3 versus Type 1)"""
    replace(dataset, tag)


def delete_or_empty_or_replace(dataset, tag):
    """
    X/Z/D - X unless Z or D is required to maintain IOD conformance (Type 3 versus Type 2 versus
    Type 1)
    """
    replace(dataset, tag)


def delete_or_empty_or_replace_UID(dataset, tag):
    """
    X/Z/U* - X unless Z or replacement of contained instance UIDs (U) is required to maintain IOD
    conformance (Type 3 versus Type 2 versus Type 1 sequences containing UID references)
    """
    element = dataset.get(tag)
    if element is not None:
        if element.VR == "UI":
            replace_element_UID(element)
        else:
            empty_element(element)


# Generation functions


@dataclass
class Action:
    function: callable
    number_of_expected_arguments: int


class ActionsMapNameFunctions(Enum):
    replace = Action(replace, 0)
    empty = Action(empty, 0)
    delete = Action(delete, 0)
    replace_UID = Action(replace_UID, 0)
    empty_or_replace = Action(empty_or_replace, 0)
    delete_or_empty = Action(delete_or_empty, 0)
    delete_or_replace = Action(delete_or_replace, 0)
    delete_or_empty_or_replace = Action(delete_or_empty_or_replace, 0)
    delete_or_empty_or_replace_UID = Action(delete_or_empty_or_replace_UID, 0)
    keep = Action(keep, 0)
    replace_with_value = Action(replace_with_value, 1)
    regexp = Action(regexp, 2)


def initialize_actions(dicom_version: str = "dicomfields_2023") -> dict:
    """
    Initialize anonymization actions with DICOM standard values

    :param dicom_version: DICOM version to use
    :return Dict object which map actions to tags
    """
    tags = dicom_anonymization_database_selector(dicom_version)

    anonymization_actions = {tag: replace for tag in tags["D_TAGS"]}
    anonymization_actions.update({tag: empty for tag in tags["Z_TAGS"]})
    anonymization_actions.update({tag: delete for tag in tags["X_TAGS"]})
    anonymization_actions.update({tag: replace_UID for tag in tags["U_TAGS"]})
    anonymization_actions.update({tag: empty_or_replace for tag in tags["Z_D_TAGS"]})
    anonymization_actions.update({tag: delete_or_empty for tag in tags["X_Z_TAGS"]})
    anonymization_actions.update({tag: delete_or_replace for tag in tags["X_D_TAGS"]})
    anonymization_actions.update(
        {tag: delete_or_empty_or_replace for tag in tags["X_Z_D_TAGS"]}
    )
    anonymization_actions.update(
        {tag: delete_or_empty_or_replace_UID for tag in tags["X_Z_U_STAR_TAGS"]}
    )
    return anonymization_actions


def initialize_actions_2024b() -> dict:
    """
    Initialize anonymization actions with DICOM standard values of 2024b.
    If you want to use 2024b version of anonymization, call anonymize_dataset with base_rules_gen=initialize_actions_2024b.

    :return Dict object which map actions to tags
    """
    return initialize_actions("dicomfields_2024b")


def anonymize_dicom_file(
    in_file: str,
    out_file: str,
    extra_anonymization_rules: dict = None,
    delete_private_tags: bool = True,
    base_rules_gen: Callable = initialize_actions,
) -> None:
    """
    Anonymize a DICOM file by modifying personal tags

    Conforms to DICOM standard except for customer specificities.

    :param in_file: File path or file-like object to read from
    :param out_file: File path or file-like object to write to
    :param extra_anonymization_rules: add more tag's actions
    :param delete_private_tags: Define if private tags should be delete or not
    """
    dataset = pydicom.dcmread(in_file)

    anonymize_dataset(
        dataset, extra_anonymization_rules, delete_private_tags, base_rules_gen
    )

    # Store modified image
    dataset.save_as(out_file)


def get_private_tag(dataset, tag):
    """
    Get the creator and element from tag

    :param dataset: Dicom dataset
    :param tag: Tag from which we want to extract private information
    :return dictionary with creator of the tag and tag element (which contains element + offset)
    """
    element = dataset.get(tag)

    element_value = element.value
    tag_group = element.tag.group
    # The element is a private creator
    if element_value in dataset.private_creators(tag_group):
        creator = {"tagGroup": tag_group, "creatorName": element.value}
        private_element = None
    # The element is a private element with an associated private creator
    else:
        # Shift the element tag in order to get the create_tag
        # 0x1009 >> 8 will give 0x0010
        create_tag_element = element.tag.element >> 8
        create_tag = pydicom.tag.Tag(tag_group, create_tag_element)
        create_dataset = dataset.get(create_tag)
        creator = {"tagGroup": tag_group, "creatorName": create_dataset.value}
        # Define which offset should be applied to the creator to find
        # this element
        # 0x0010 << 8 will give 0x1000
        offset_from_creator = element.tag.element - (create_tag_element << 8)
        private_element = {"element": element, "offset": offset_from_creator}

    return {"creator": creator, "element": private_element}


def get_private_tags(
    anonymization_actions: dict, dataset: pydicom.Dataset
) -> List[dict]:
    """
    Extract private tag as a list of object with creator and element

    :param anonymization_actions: list of tags associated to an action
    :param dataset: Dicom dataset which will be anonymize and contains all private tags
    :return Array of object
    """
    private_tags = []
    for tag in anonymization_actions.keys():
        try:
            element = dataset.get(tag)
        except KeyError:
            print("Cannot get element from tag: ", tag_to_hex_strings(tag))

        if element and element.tag.is_private:
            private_tags.append(get_private_tag(dataset, tag))

    return private_tags


def anonymize_dataset(
    dataset: pydicom.Dataset,
    extra_anonymization_rules: dict = None,
    delete_private_tags: bool = True,
    base_rules_gen: Callable = initialize_actions,
) -> None:
    """
    Anonymize a pydicom Dataset by using anonymization rules which links an action to a tag

    :param dataset: Dataset to be anonymize
    :param base_rules_gen: Function to generate the base rules
    :param extra_anonymization_rules: Rules to be applied on the dataset
    :param delete_private_tags: Define if private tags should be delete or not
    """
    current_anonymization_actions = base_rules_gen()

    if extra_anonymization_rules is not None:
        current_anonymization_actions.update(extra_anonymization_rules)

    private_tags = []

    for tag, action in current_anonymization_actions.items():

        def range_callback(dataset, data_element):
            if (
                data_element.tag.group & tag[2] == tag[0] & tag[2]
                and data_element.tag.element & tag[3] == tag[1] & tag[3]
            ):
                tag_tuple = (data_element.tag.group, data_element.tag.element)
                action(dataset, tag_tuple)
                if dataset.get(tag_tuple) and data_element.is_private:
                    private_tags.append(get_private_tag(dataset, tag_tuple))

        element = None

        # We are in a repeating group
        if len(tag) > 2:
            dataset.walk(range_callback)
        # Individual Tags
        else:
            # From : https://github.com/KitwareMedical/dicom-anonymizer/pull/18
            # The meta header information is located in the `file_meta` dataset
            # For tags with tag group `0x0002` we thus apply the action to the `file_meta` dataset
            if tag[0] == 0x0002:
                if not hasattr(dataset, "file_meta"):
                    continue
                # Apply rule to meta information header
                action(dataset.file_meta, tag)
            else:
                action(dataset, tag)

            try:
                element = dataset.get(tag)
            except KeyError:
                print("Cannot get element from tag: ", tag_to_hex_strings(tag))
                continue

            # Get private tag to restore it later
            if element and element.tag.is_private:
                private_tags.append(get_private_tag(dataset, tag))

    # X - Private tags = (0xgggg, 0xeeee) where 0xgggg is odd
    if delete_private_tags:
        dataset.remove_private_tags()

        # Adding back private tags if specified in dictionary
        for privateTag in private_tags:
            creator = privateTag["creator"]
            element = privateTag["element"]
            block = dataset.private_block(
                creator["tagGroup"], creator["creatorName"], create=True
            )
            if element is not None:
                block.add_new(
                    element["offset"], element["element"].VR, element["element"].value
                )
