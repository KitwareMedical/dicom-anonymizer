import argparse
import ast
import json
import os
import re
import tqdm

from .simpledicomanonymizer import *

def main(map = {}):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('input', help='Path to the input dicom file or input directory which contains dicom files')
    parser.add_argument('output', help='Path to the output dicom file or output directory which will contains dicom files')
    parser.add_argument('-t', action='append', nargs='*', help='tags action : Defines a new action to apply on the tags list')
    parser.add_argument('--dictionary', action='store', help='File which contains a dictionary that can be added to the original one')
    args = parser.parse_args()

    # Get input arguments
    InputPath = args.input
    OutputPath = args.output
    InputFolder = ''
    OutputFolder = ''

    if os.path.isdir(InputPath):
        InputFolder = InputPath

    if os.path.isdir(OutputPath):
        OutputFolder = OutputPath
        if InputFolder == '':
            OutputPath = OutputFolder + os.path.basename(InputPath)

    if InputFolder != '' and OutputFolder == '':
        print('Error, please set an output folder path with an input folder path')
        return

    # Create a new actions' dictionary from input parameters
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
            cpt = 0
            for k, v in data.items():
                l = [ast.literal_eval(k)]
                actionFunction = map[v] if v in map else eval(v)
                if cpt == 0:
                    newAnonymizationActions = generateActions(l, actionFunction)
                else:
                    newAnonymizationActions.update(generateActions(l, actionFunction))
                cpt += 1


    # Generate list of input file if a folder has been set
    inputFilesList = []
    outputFilesList = []
    if InputFolder == '':
        inputFilesList.append(InputPath)
        outputFilesList.append(OutputPath)
    else:
        files = os.listdir(InputFolder)
        for fileName in files:
            inputFilesList.append(InputFolder + '/' + fileName)
            outputFilesList.append(OutputFolder + '/' + fileName)

    progressBar = tqdm.tqdm(total=len(inputFilesList))
    for cpt in range(len(inputFilesList)):
        # print('Process ' + str(cpt + 1) + '//' + str(len(inputFilesList)))
        anonymizeDICOMFile(inputFilesList[cpt], outputFilesList[cpt], newAnonymizationActions)
        progressBar.update(1)

    progressBar.close()
