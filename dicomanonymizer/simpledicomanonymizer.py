import re
import pydicom
from random import randint

from .dicomfields import *

dictionary = {}

# Regexp function

def regexp(options: dict):
    """
    Apply a regexp method to the dataset

    :param options: contains two values:
        - find: which string should be find
        - replace: string that will replace the find string
    """
    def apply_regexp(dataset, tag):
        """
        Apply a regexp to the dataset
        """
        element = dataset.get(tag)
        if element is not None:
            element.value = re.sub(options['find'], options['replace'], str(element.value))

    return apply_regexp

# Default anonymization functions

def replace_element_UID(element):
    """
    Keep char value but replace char number with random number
    The replaced value is kept in a dictionary link to the initial element.value in order to automatically
    apply the same replaced value if we have an other UID with the same value
    """
    if element.value not in dictionary:
        new_chars = [str(randint(0, 9)) if char.isalnum() else char for char in element.value]
        dictionary[element.value] = ''.join(new_chars)
    element.value = dictionary.get(element.value)


def replace_element_date(element):
    """
    Replace date element's value with '00010101'
    """
    element.value = '00010101'


def replace_element_date_time(element):
    """
    Replace date time element's value with '00010101010101.000000+0000'
    """
    element.value = '00010101010101.000000+0000'


def replace_element(element):
    """
    Replace element's value according to it's VR:
    - DA: cf replace_element_date
    - TM: replace with '000000.00'
    - LO, SH, PN, CS: replace with 'Anonymized'
    - UI: cf replace_element_UID
    - IS: replace with '0'
    - SS: replace with 0
    - SQ: call replace_element for all sub elements
    - DT: cf replace_element_date_time
    """
    if element.VR == 'DA':
        replace_element_date(element)
    elif element.VR == 'TM':
        element.value = '000000.00'
    elif element.VR in ('LO', 'SH', 'PN', 'CS'):
        element.value = 'Anonymized'
    elif element.VR == 'UI':
        replace_element_UID(element)
    elif element.VR == 'UL':
        pass
    elif element.VR == 'IS':
        element.value = '0'
    elif element.VR == 'SS':
        element.value = 0
    elif element.VR == 'SQ':
        for sub_dataset in element.value:
            for sub_element in sub_dataset.elements():
                replace_element(sub_element)
    elif element.VR == 'DT':
        replace_element_date_time(element)
    else:
        raise NotImplementedError('Not anonymized. VR {} not yet implemented.'.format(element.VR))


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
    - SH, PN, UI, LO, CS: value will be set to ''
    - DA: value will be replaced by '00010101'
    - TM: value will be replaced by '000000.00'
    - UL: value will be replaced by 0
    - SQ: all subelement will be called with "empty_element"
    """
    if (element.VR in ('SH', 'PN', 'UI', 'LO', 'CS')):
        element.value = ''
    elif element.VR == 'DA':
        replace_element_date(element)
    elif element.VR == 'TM':
        element.value = '000000.00'
    elif element.VR == 'UL':
        element.value = 0
    elif element.VR == 'SQ':
        for sub_dataset in element.value:
            for sub_element in sub_dataset.elements():
                empty_element(sub_element)
    else:
        raise NotImplementedError('Not anonymized. VR {} not yet implemented.'.format(element.VR))


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
    if element.VR == 'DA':
        replace_element_date(element)
    elif element.VR == 'SQ':
        for sub_dataset in element.value:
            for sub_element in sub_dataset.elements():
                delete_element(sub_dataset, sub_element)
    else:
        del dataset[element.tag]


def delete(dataset, tag):
    """X - remove"""
    def range_callback(dataset, data_element):
        if data_element.tag.group & tag[2] == tag[0] and data_element.tag.element & tag[3] == tag[1]:
            delete_element(dataset, data_element)

    if len(tag) > 2:  # Tag ranges
        dataset.walk(range_callback)
    else:  # Individual Tags
        element = dataset.get(tag)
        if element is not None:
            delete_element(dataset, element)  # element.tag is not the same type as tag.


def keep(dataset, tag):
    """K - keep (unchanged for non-sequence attributes, cleaned for sequences)"""
    pass


def clean(dataset, tag):
    """
    C - clean, that is replace with values of similar meaning known not to contain identifying
    information and consistent with the VR
    """
    if dataset.get(tag) is not None:
        raise NotImplementedError('Tag not anonymized. Not yet implemented.')


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
        if element.VR == 'UI':
            replace_element_UID(element)
        else:
            empty_element(element)

# Generation functions

actions_map_name_functions = {
    "replace": replace,
    "empty": empty,
    "delete": delete,
    "replace_UID": replace_UID,
    "empty_or_replace": empty_or_replace,
    "delete_or_empty": delete_or_empty,
    "delete_or_replace": delete_or_replace,
    "delete_or_empty_or_replace": delete_or_empty_or_replace,
    "delete_or_empty_or_replace_UID": delete_or_empty_or_replace_UID,
    "keep": keep,
    "regexp": regexp
}

def generate_actions(tag_list:list, action, options: dict =None) -> dict:
    """
    Generate a dictionary using list values as tag and assign the same value to all

    :param tag_list: list of tags which will have the same associated actions
    :param action: define the action that will be use. It can be a callable custom function or a name of a pre-defined
    action from simpledicomanonymizer.
    :param options: Define options tht will be affected to the action (like regexp)
    """
    final_action = action
    if not callable(action):
        final_action = actions_map_name_functions[action] if action in actions_map_name_functions else keep
    if options is not None:
        final_action = final_action(options)
    return {tag: final_action for tag in tag_list}


def initialize_actions() -> dict:
    """
    Initialize anonymization actions with DICOM standard values

    :return Dict object which map actions to tags
    """
    anonymization_actions = generate_actions(D_TAGS, replace)
    anonymization_actions.update(generate_actions(Z_TAGS, empty))
    anonymization_actions.update(generate_actions(X_TAGS, delete))
    anonymization_actions.update(generate_actions(U_TAGS, replace_UID))
    anonymization_actions.update(generate_actions(Z_D_TAGS, empty_or_replace))
    anonymization_actions.update(generate_actions(X_Z_TAGS, delete_or_empty))
    anonymization_actions.update(generate_actions(X_D_TAGS, delete_or_replace))
    anonymization_actions.update(generate_actions(X_Z_D_TAGS, delete_or_empty_or_replace))
    anonymization_actions.update(generate_actions(X_Z_U_STAR_TAGS, delete_or_empty_or_replace_UID))
    return anonymization_actions


def anonymize_dicom_file(in_file: str, out_file: str, extra_anonymization_rules: dict = None, delete_private_tags: bool = True) -> None:
    """
    Anonymize a DICOM file by modifying personal tags

    Conforms to DICOM standard except for customer specificities.

    :param in_file: File path or file-like object to read from
    :param out_file: File path or file-like object to write to
    :param extra_anonymization_rules: add more tag's actions
    :param delete_private_tags: Define if private tags should be delete or not
    """
    dataset = pydicom.dcmread(in_file)

    anonymize_dataset(dataset, extra_anonymization_rules, delete_private_tags)

    # Store modified image
    dataset.save_as(out_file)


def anonymize_dataset(dataset: pydicom.Dataset, extra_anonymization_rules: dict = None, deletePrivateTags: bool = True) -> None:
    """
    Anonymize a pydicom Dataset by using anonymization rules which links an action to a tag

    :param dataset: Dataset to be anonymize
    :param extra_anonymization_rules: Rules to be applied on the dataset
    :param delete_private_tags: Define if private tags should be delete or not
    """
    current_anonymization_actions = initialize_actions()

    if extra_anonymization_rules is not None:
        current_anonymization_actions.update(extra_anonymization_rules)

    for tag, action in current_anonymization_actions.items():
        action(dataset, tag)

    # X - Private tags = (0xgggg, 0xeeee) where 0xgggg is odd
    if deletePrivateTags:
        dataset.remove_private_tags()
