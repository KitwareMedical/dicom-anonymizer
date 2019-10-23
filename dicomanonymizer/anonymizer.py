import argparse
import ast
import json
import os
import re

from .simpledicomanonymizer import *

def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('input', help='Path to the input dicom file')
    parser.add_argument('output', help='Path to the output dicom file')
    parser.add_argument('-t', action='append', nargs='*', help='tags action : Defines a new action to apply on the tags list')
    parser.add_argument('--dictionary', action='store', help='File which contains a dictionary that can be added to the original one')
    parser.add_argument('--inputFolder', action='store', help='Path to a folder that contains DICOM file to be anonymized')
    parser.add_argument('--outputFolder', action='store', help='Path to a folder that contains anonymized DICOM file')
    args = parser.parse_args()

    # Get input arguments
    InputFilePath = args.input
    OutputFilePath = args.output
    InputFolder = ''
    OutputFolder = ''
    if args.inputFolder and args.outputFolder:
        InputFolder = args.inputFolder
        OutputFolder = args.outputFolder

    # Create a new actions' dictionary from parameters
    newAnonymizationActions = ''
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

                if i == 0:
                    newAnonymizationActions = generateActions(tagsList, eval(actionName))
                else:
                    newAnonymizationActions.update(generateActions(tagsList, eval(actionName)))

    # Read an existing dictionary
    if args.dictionary:
        with open(args.dictionary) as json_file:
            data = json.load(json_file)
            for k, v in data.items():
                l = [ast.literal_eval(k)]
                newAnonymizationActions.update(generateActions(l, eval(v)))


    # Generate list of input file if a folder has been set
    inputFilesList = []
    outputFilesList = []
    if InputFolder == '':
        inputFilesList.append(InputFilePath)
        outputFilesList.append(OutputFilePath)
    else:
        files = os.listdir(InputFolder)
        for fileName in files:
            inputFilesList.append(InputFolder + '\\' + fileName)
            outputFilesList.append(OutputFolder + '\\' + fileName)

    for cpt in range(len(inputFilesList)):
        print('Process ' + str(cpt) + '//' + str(len(inputFilesList)))
        anonymizeDICOMFile(inputFilesList[cpt], outputFilesList[cpt], newAnonymizationActions)
