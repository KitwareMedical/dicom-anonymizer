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
        print('Error, please set an output folder path with an input folder path')
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
    for tag in mapActionTag.iterkeys():
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
    parser.add_argument('-t', action='append', nargs='*', help='tags action : Defines a new action to apply on the tags list')
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
                actionName = args.t[i].pop()
                if len(args.t[i]) == 0:
                    continue
                tagsList = []
                for tag in args.t[i]:
                    tagsList.append(ast.literal_eval(tag))

                if cpt == 0:
                    newAnonymizationActions = generateActions(tagsList, eval(actionName))
                else:
                    newAnonymizationActions.update(generateActions(tagsList, eval(actionName)))
                cpt += 1

    # Read an existing dictionary
    if args.dictionary:
        with open(args.dictionary) as json_file:
            data = json.load(json_file)
            for k, v in data.items():
                l = [ast.literal_eval(k)]
                actionFunction = definedActionMap[v] if v in definedActionMap else eval(v)
                if cpt == 0:
                    newAnonymizationActions = generateActions(l, actionFunction)
                else:
                    newAnonymizationActions.update(generateActions(l, actionFunction))
                cpt += 1

    # Launch the anonymization
    anonymize(InputPath, OutputPath, newAnonymizationActions)
