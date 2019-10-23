
  

# DicomAnonymizer

  

## Introduction

  

This is a python package to anonymize DICOM files.

  

The default behaviour of this package is to anonymize DICOM fields referenced in dicomfields.py.

  

More information about dicom fields can be found [here](http://dicom.nema.org/dicom/2013/output/chtml/part15/chapter_E.html#table_E.1-1)

  
  

## Build it

  

The sources files can be packaged by using this command line :

  

`python .\setup.py bdist_wheel`

  

This command will generate a wheel package in 'dist' folder which can be then installed as a python package using

  

`pip install .\dist\DicomAnonymizer-0.0.1-py2.py3-none-any.whl`

  

Installing this package will also install an executable named `dicom-anonymizer`. In order to use it, please refer to the next section.

  

## How to use it ?

  

This package allows to anonymize a selection of DICOM field (defined or overrided). The way on how the DICOM fields are anonymized can also be overrided.

```
InputFilePath = Full path to a single DICOM image
OutputFilePath = Full path to the anonymized DICOM image
ActionName = Defined an action name that will be applied to the DICOM tag. 
```



### Default behaviour

**Executable**:
`dicom-anonymizer InputFilePath OutputFilePath`

**Code**:
Create file anonymizerUser.py which contains :
```python
import dicomanonymizer.anonymizer
dicomanonymizer.anonymizer.main()
```
Call this file with arguments :
```python
python anonymizerUser.py InputFilePath OutputFilePath
```



### Custom rules
You can manually add new rules :
**Executable**:
```python
dicom-anonymizer InputFilePath OutputFilePath -t '(0x0001, 0x0001)' ActionName -t '(0x0001, 0x0005)' ActionName2
```
**Code**
```python
python anonymizer.py InputFilePath OutputFilePath -t '(0x0001, 0x0001)' ActionName -t '(0x0001, 0x0005)' ActionName2
```
This will apply the `ActionName` to the tag `'(0x0001, 0x0001)'` and `ActionName2` to `'(0x0001, 0x0005)'`

**Note**: ActionName has to be defined in [actions list](##Actions-list)

### :point_right:Custom rules with dictionary file
Instead of have a big command line, you can create your own dictionary by creating a json file `dictionary.json` :
```json
{
    "(0x0002, 0x0002)": "ActionName",
    "(0x0003, 0x0003)": "ActionName",
    "(0x0004, 0x0004)": "ActionName",
    "(0x0005, 0x0005)": "ActionName"
}
```
Same as before, the `ActionName` has to be defined in the actions list.

**Executable**
```python
python anonymizerUser.py InputFilePath OutputFilePath --dictionary dictionary.json
```
### Custom actions from dictionary file

If you use the file anonymizerUser.py, then you can add custom actions:
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

def ActionNameNotReferenced:
	print('custom action')
def ActionNameNotReferenced1:
	print('custom action 1')
def ActionNameNotReferenced2:
	print('custom action 2')

dicomanonymizer.anonymizer.main()
```
**Code**
```python
python anonymizerUser.py InputFilePath OutputFilePath --dictionary dictionary.json
```



**Executable**
:warning: This won't work if you use the executable because the package doesn't know the cutom actions
```python
python anonymizerUser.py InputFilePath OutputFilePath --dictionary dictionary.json
```

## Actions list
- replaceElementUID
- replaceElementDate
- replaceElementDateTime
- replaceElement
- replace
- emptyElement
- empty
- deleteElement
- delete
- keep
- clean
- replaceUID
- emptyOrReplace
- deleteOrEmpty
- deleteOrReplace
- deleteOrEmplyOrReplace
- deleteOrEmptyOrReplaceUID