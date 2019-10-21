# authors :
# Guillaume Lemaitre <g.lemaitre58@gmail.com>,
# Edern Haumont <edern.haumont@kitware.com>
# license : MIT

from importlib import import_module
import re
import pydicom
import sys

from DicomFields import *


# Default anonymization functions

def replaceElementUID(element):
    element.value = re.sub(r'\d', '1', element.value)


def replaceElementDate(element):
    element.value = '00010101'


def replaceElementDateTime(element):
    element.value = '00010101010101.000000+0000'


def replaceElement(element):
    if element.VR == 'DA':
        replaceElementDate(element)
    elif element.VR == 'TM':
        element.value = '000000.00'
    elif element.VR in ('LO', 'SH', 'PN', 'CS'):
        element.value = 'Anonymized'
    elif element.VR == 'UI':
        replaceElementUID(element)
    elif element.VR == 'UL':
        pass
    elif element.VR == 'IS':
        element.value = '0'
    elif element.VR == 'SS':
        element.value = 0
    elif element.VR == 'SQ':
        for subDataset in element.value:
            for subElement in subDataset.elements():
                replaceElement(subElement)
    elif element.VR == 'DT':
        replaceElementDateTime(element)
    else:
        raise NotImplementedError('Not anonymized. VR {} not yet implemented.'.format(element.VR))


def replace(dataset, tag):
    """
    D - replace with a non-zero length value that may be a dummy value and consistent with the
    VR
    """
    element = dataset.get(tag)
    if element is not None:
        replaceElement(element)


def emptyElement(element):
    if (element.VR in ('SH', 'PN', 'UI', 'LO', 'CS')):
        element.value = ''
    elif element.VR == 'DA':
        replaceElementDate(element)
    elif element.VR == 'TM':
        element.value = '000000.00'
    elif element.VR == 'UL':
        element.value = 0
    elif element.VR == 'SQ':
        for subDataset in element.value:
            for subElement in subDataset.elements():
                emptyElement(subElement)
    else:
        raise NotImplementedError('Not anonymized. VR {} not yet implemented.'.format(element.VR))


def empty(dataset, tag):
    """
    Z - replace with a zero length value, or a non-zero length value that may be a dummy value and
    consistent with the VR
    """
    element = dataset.get(tag)
    if element is not None:
        emptyElement(element)


def deleteElement(dataset, element):
    if element.VR == 'DA':
        replaceElementDate(element)
    elif element.VR == 'SQ':
        for subDataset in element.value:
            for subElement in subDataset.elements():
                deleteElement(subDataset, subElement)
    else:
        del dataset[element.tag]


def delete(dataset, tag):
    """X - remove"""
    def rangeCallback(dataset, dataElement):
        if dataElement.tag.group & tag[2] == tag[0] and dataElement.tag.element & tag[3] == tag[1]:
            deleteElement(dataset, dataElement)

    if (len(tag) > 2):  # Tag ranges
        dataset.walk(rangeCallback)
    else:  # Individual Tags
        element = dataset.get(tag)
        if element is not None:
            deleteElement(dataset, element)  # element.tag is not the same type as tag.


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


def replaceUID(dataset, tag):
    """
    U - replace with a non-zero length UID that is internally consistent within a set of Instances
    Lazy solution : Replace with empty string
    """
    element = dataset.get(tag)
    if element is not None:
        replaceElementUID(element)


def emptyOrReplace(dataset, tag):
    """Z/D - Z unless D is required to maintain IOD conformance (Type 2 versus Type 1)"""
    replace(dataset, tag)


def deleteOrEmpty(dataset, tag):
    """X/Z - X unless Z is required to maintain IOD conformance (Type 3 versus Type 2)"""
    empty(dataset, tag)


def deleteOrReplace(dataset, tag):
    """X/D - X unless D is required to maintain IOD conformance (Type 3 versus Type 1)"""
    replace(dataset, tag)


def deleteOrEmptyOrReplace(dataset, tag):
    """
    X/Z/D - X unless Z or D is required to maintain IOD conformance (Type 3 versus Type 2 versus
    Type 1)
    """
    replace(dataset, tag)


def deleteOrEmptyOrReplaceUID(dataset, tag):
    """
    X/Z/U* - X unless Z or replacement of contained instance UIDs (U) is required to maintain IOD
    conformance (Type 3 versus Type 2 versus Type 1 sequences containing UID references)
    """
    element = dataset.get(tag)
    if element is not None:
        if element.VR == 'UI':
            replaceElementUID(element)
        else:
            emptyElement(element)


# Generation functions

def generateActions(tagList, action):
    """Generate a dictionnary using list values as tag and assign the same value to all
    :type tagList: list
    """
    return {tag: action for tag in tagList}


def initializeActions():
    """Initialize anonymization actions with DICOM standard values
    """
    anonymizationActions = generateActions(D_TAGS, replace)
    anonymizationActions.update(generateActions(Z_TAGS, empty))
    anonymizationActions.update(generateActions(X_TAGS, delete))
    anonymizationActions.update(generateActions(U_TAGS, replaceUID))
    anonymizationActions.update(generateActions(Z_D_TAGS, emptyOrReplace))
    anonymizationActions.update(generateActions(X_Z_TAGS, deleteOrEmpty))
    anonymizationActions.update(generateActions(X_D_TAGS, deleteOrReplace))
    anonymizationActions.update(generateActions(X_Z_D_TAGS, deleteOrEmptyOrReplace))
    anonymizationActions.update(generateActions(X_Z_U_STAR_TAGS, deleteOrEmptyOrReplaceUID))
    return anonymizationActions

def anonymizeDICOMFile(inFile, outFile, dictionary = ''):
    """Anonymize a DICOM file by modyfying personal tags

    Conforms to DICOM standard except for customer specificities.

    :param inFile: File path or file-like object to read from
    :param outFile: File path or file-like object to write to
    :param dictionary: add more tag's actions
    """

    currentAnonymizationActions = initializeActions()

    if dictionary != '':
        currentAnonymizationActions.update(dictionary)

    dataset = pydicom.dcmread(inFile)

    for tag, action in currentAnonymizationActions.items():
        action(dataset, tag)

    # X - Private tags = (0xgggg, oxeeee) where 0xgggg is odd
    dataset.remove_private_tags()

    # Store modified image
    dataset.save_as(outFile)
