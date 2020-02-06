# DicomAnonymizer

Python package to anonymize DICOM files.
The anonymization answer to the standard . More information about dicom fields for anonymization can be found [here](http://dicom.nema.org/dicom/2013/output/chtml/part15/chapter_E.html#table_E.1-1).

The default behaviour of this package is to anonymize DICOM fields referenced in [dicomfields](dicomanonymizer/dicomfields.py).

Dicom fields are separated into different groups. Each groups will be anonymized in a different way.

| Group | Action | Action definition |
| --- | --- | --- |
| D_TAGS | replace | Replace with a non-zero length value that may be a dummy value and consistent with the VR** |
| Z_TAGS | empty | Replace with a zero length value, or a non-zero length value that may be a dummy value and consistent with the VR** |
| X_TAGS | delete | Completely remove the tag |
| U_TAGS | replaceUID | Replace all UID's number with a random one in order to keep consistent. Same UID will have the same replaced value |
| Z_D_TAGS | emptyOrReplace | Replace with a non-zero length value that may be a dummy value and consistent with the VR** |
| X_Z_TAGS | deleteOrEmpty | Replace with a zero length value, or a non-zero length value that may be a dummy value and consistent with the VR** |
| X_D_TAGS | deleteOrReplace | Replace with a non-zero length value that may be a dummy value and consistent with the VR** |
| X_Z_D_TAGS | deleteOrEmptyOrReplace | Replace with a non-zero length value that may be a dummy value and consistent with the VR** |
| X_Z_U_STAR_TAGS | deleteOrEmptyOrReplaceUID | If it's a UID, then all numbers are randomly replaced. Else, replace with a zero length value, or a non-zero length value that may be a dummy value and consistent with the VR**|



# How to build it ?

The sources files can be packaged by using:
`python .\setup.py bdist_wheel`

This command will generate a wheel package in `dist` folder which can be then installed as a python package using
`pip install .\dist\DicomAnonymizer-0.0.1-py2.py3-none-any.whl`

Installing this package will also install an executable named `dicom-anonymizer`. In order to use it, please refer to the next section.



# How to use it ?

This package allows to anonymize a selection of DICOM field (defined or overrided).
The way on how the DICOM fields are anonymized can also be overrided.

**[required]** InputPath = Full path to a single DICOM image or to a folder which contains dicom files
**[required]** OutputPath = Full path to the anonymized DICOM image or to a folder. This folder has to exist.
**[optional] **ActionName = Defined an action name that will be applied to the DICOM tag.
**[optional]** Dictionary = Path to a JSON file which defines actions that will be applied on specific dicom tags (see below)



## Default behaviour

You can use the default anonymization behaviour describe above.

```python
dicom-anonymizer Input Output
```



## Custom rules
You can manually add new rules in order to have different behaviors with certain tags.
This will allow you to override default rules :

**Executable**:
```python
dicom-anonymizer InputFilePath OutputFilePath -t '(0x0001, 0x0001)' ActionName -t '(0x0001, 0x0005)' ActionName2
```
This will apply the `ActionName` to the tag `'(0x0001, 0x0001)'` and `ActionName2` to `'(0x0001, 0x0005)'`

**Note**: ActionName has to be defined in [actions list](#actions-list)

For example, the default behavior of the patient's ID is to be replaced by an empty or null value. If you want to keep this value, then you'll have to run :
```python
python anonymizer.py InputFilePath OutputFilePath -t '(0x0010, 0x0020)' keep
```
This command will override the default behavior executed on this tag and the patient's ID will be kept.



## Custom rules with dictionary file

Instead of having a big command line with several new actions, you can create your own dictionary by creating a json file `dictionary.json` :
```json
{
    "(0x0002, 0x0002)": "ActionName",
    "(0x0003, 0x0003)": "ActionName",
    "(0x0004, 0x0004)": "ActionName",
    "(0x0005, 0x0005)": "ActionName"
}
```
Same as before, the `ActionName` has to be defined in the [actions list](#actions-list).

```python
dicom-anonymizer InputFilePath OutputFilePath --dictionary dictionary.json
```


## Custom actions from dictionary file

If you use the file anonymizer.py, then you can add custom actions:
```json
{
    "(0x0002, 0x0002)": "ActionNameNotReferenced",
    "(0x0003, 0x0003)": "ActionNameNotReferenced",
    "(0x0004, 0x0004)": "ActionNameNotReferenced1",
    "(0x0005, 0x0005)": "ActionNameNotReferenced2"
}
```
Then, modify your file anonymizerUser.py :
```python
import dicomanonymizer.anonymizer

# Functions need to have in input a dataset and a tag
def ActionNameNotReferenced(dataset, tag):
    # Extract the element from the dataset :
    element = dataset.get(tag)
    # You can update the value as here :
    element.value = ''
	print('custom action')
def ActionNameNotReferenced1(dataset, tag):
	print('custom action 1')
def ActionNameNotReferenced2(dataset, tag):
	print('custom action 2')

actionsTagMap = {
	(0x0001, 0x0001): "keep", #will use the default method in the dicom anonymizer
	(0x0002, 0x0002): ActionNameNotReferenced,
	(0x0003, 0x0003): ActionNameNotReferenced2
}

# Generate a custom dictionary that will be override the default one
actionsMap = dicomanonymizer.anonymizer.generateActionsDictionary(actionsTagMap)

# Send the map to the main function
dicomanonymizer.anonymizer.anonymize(actionsMap)
```

In your own file, you'll have to define:
- Your custom functions. Be careful, your functions always have in inputs a dataset and a tag
- A dictionary which map your functions to a string

# Overrides actions for default tags
You can have the need to keep some tags, for example UID. Then, instead of replace it (`replaceUID` action) then you can override it :
```
UIDActionMap = dicomanonymizer.simpledicomanonymizer.generateActions(dicomanonymizer.dicomfields.U_TAGS, "keep")
dicomanonymizer.anonymizer.anonymize(inFile, outFile, actionsMap)
```
All the listed actions below can be used with `generateActions` function by using a string. If the second parameter of the `generateActions` actions is a string and doesn't belong to the actions list, then the default behaviour will be to keep the tag.

# Actions list

| Action | Action definition |
| --- | --- |
| empty | Replace with a zero length value, or a non-zero length value that may be a dummy value and consistent with the VR** |
| delete | Completely remove the tag |
| keep | Do nothing on the tag |
| clean | Don't use it for now. This is not implemented |
| replaceUID | Replace all UID's number with a random one in order to keep consistent. Same UID will have the same replaced value |
| emptyOrReplace | Replace with a non-zero length value that may be a dummy value and consistent with the VR** |
| deleteOrEmpty | Replace with a zero length value, or a non-zero length value that may be a dummy value and consistent with the VR** |
| deleteOrReplace | Replace with a non-zero length value that may be a dummy value and consistent with the VR** |
| deleteOrEmplyOrReplace | Replace with a non-zero length value that may be a dummy value and consistent with the VR** |
| deleteOrEmptyOrReplaceUID | If it's a UID, then all numbers are randomly replaced. Else, replace with a zero length value, or a non-zero length value that may be a dummy value and consistent with the VR** |


** VR: Value Representation
