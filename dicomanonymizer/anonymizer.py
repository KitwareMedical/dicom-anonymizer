import argparse
import ast
import json
import os
import re
import tqdm

from .simpledicomanonymizer import *

def anonymize(inputPath, outputPath, anonymizationActions):
    # Get input arguments
    InputFolder = ''
    OutputFolder = ''

    if os.path.isdir(inputPath):
        InputFolder = inputPath

    if os.path.isdir(outputPath):
        OutputFolder = outputPath
        if InputFolder == '':
            outputPath = OutputFolder + os.path.basename(inputPath)

    if InputFolder != '' and OutputFolder == '':
        print('Error, please set a correct output folder path')
        sys.exit()

    # Generate list of input file if a folder has been set
    inputFilesList = []
    outputFilesList = []
    if InputFolder == '':
        inputFilesList.append(inputPath)
        outputFilesList.append(outputPath)
    else:
        files = os.listdir(InputFolder)
        for fileName in files:
            inputFilesList.append(InputFolder + '/' + fileName)
            outputFilesList.append(OutputFolder + '/' + fileName)

    progressBar = tqdm.tqdm(total=len(inputFilesList))
    for cpt in range(len(inputFilesList)):
        anonymizeDICOMFile(inputFilesList[cpt], outputFilesList[cpt], anonymizationActions)
        progressBar.update(1)

    progressBar.close()


def generateActionsDictionary(mapActionTag, definedActionMap = {}):
    generatedMap = {}
    cpt = 0
    for tag in mapActionTag:
        test = [tag]
        action = mapActionTag[tag]

        # Define the associated function to the tag
        if callable(action):
            actionFunction = action
        else:
            actionFunction = definedActionMap[action] if action in definedActionMap else eval(action)

        # Generate the map
        if cpt == 0:
            generatedMap = generateActions(test, actionFunction)
        else:
            generatedMap.update(generateActions(test, actionFunction))
        cpt += 1

    return generatedMap


def main(definedActionMap = {}):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('input', help='Path to the input dicom file or input directory which contains dicom files')
    parser.add_argument('output', help='Path to the output dicom file or output directory which will contains dicom files')
    parser.add_argument('-t', action='append', nargs='*', help='tags action : Defines a new action to apply on the tag.'\
    '\'regexp\' action takes two arguments: '\
        '1. regexp to find substring '\
        '2. the string that will replace the previous found string')
    parser.add_argument('--dictionary', action='store', help='File which contains a dictionary that can be added to the original one')
    args = parser.parse_args()

    InputPath = args.input
    OutputPath = args.output

    # Create a new actions' dictionary from parameters
    newAnonymizationActions = {}
    cpt = 0
    if args.t:
        numberOfNewTagsActions = len(args.t)
        if numberOfNewTagsActions > 0:
            for i in range(numberOfNewTagsActions):
                currentTagParameters = args.t[i]

                nbParameters = len(currentTagParameters)
                if nbParameters == 0:
                    continue

                options = None
                actionName = currentTagParameters[1]

                # Means that we are in regexp mode
                if nbParameters == 4:
                    options = {
                        "find": currentTagParameters[2],
                        "replace": currentTagParameters[3]
                    }

                tagsList = [ast.literal_eval(currentTagParameters[0])]

                action = eval(actionName)
                # When generateActions is called and we have options, we don't want use regexp
                # as an action but we want to call it to generate a new method
                if options is not None:
                    action = actionName

                if cpt == 0:
                    newAnonymizationActions = generateActions(tagsList, action, options)
                else:
                    newAnonymizationActions.update(generateActions(tagsList, action, options))
                cpt += 1

    # Read an existing dictionary
    if args.dictionary:
        with open(args.dictionary) as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                actionName = value
                options = None
                if type(value) is dict:
                    actionName = value['action']
                    options = {
                        "find": value['find'],
                        "replace" : value['replace']
                    }

                l = [ast.literal_eval(key)]
                action = definedActionMap[actionName] if actionName in definedActionMap else eval(actionName)
                if cpt == 0:
                    newAnonymizationActions = generateActions(l, action, options)
                else:
                    newAnonymizationActions.update(generateActions(l, action, options))
                cpt += 1

    # Launch the anonymization
    anonymize(InputPath, OutputPath, newAnonymizationActions)
