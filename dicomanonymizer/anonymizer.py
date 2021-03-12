import argparse
import ast
import json
import os
import sys
import tqdm

from .simpledicomanonymizer import *

def anonymize(input_path: str, output_path: str, anonymization_actions: dict) -> None:
    """
    Read data from input path (folder or file) and launch the anonymization.

    :param input_path: Path to a folder or to a file. If set to a folder,
    then cross all over subfiles and apply anonymization
    :param output_path: Path to a folder or to a file.
    :param anonymization_actions: List of actions that will be applied on tags
    """
    # Get input arguments
    input_folder = ''
    output_folder = ''

    if os.path.isdir(input_path):
        input_folder = input_path

    if os.path.isdir(output_path):
        output_folder = output_path
        if input_folder == '':
            output_path = output_folder + os.path.basename(input_path)

    if input_folder != '' and output_folder == '':
        print('Error, please set a correct output folder path')
        sys.exit()

    # Generate list of input file if a folder has been set
    input_files_list = []
    output_files_list = []
    if input_folder == '':
        input_files_list.append(input_path)
        output_files_list.append(output_path)
    else:
        files = os.listdir(input_folder)
        for fileName in files:
            input_files_list.append(input_folder + '/' + fileName)
            output_files_list.append(output_folder + '/' + fileName)

    progress_bar = tqdm.tqdm(total=len(input_files_list))
    for cpt in range(len(input_files_list)):
        anonymize_dicom_file(input_files_list[cpt], output_files_list[cpt], anonymization_actions, deletePrivateTags)
        progress_bar.update(1)

    progress_bar.close()


def generate_actions_dictionary(map_action_tag, defined_action_map = {}) -> dict:
    """
    Generate a new dictionary which maps actions function to tags

    :param map_action_tag: link actions to tags
    :param defined_action_map: link action name to action function
    """
    generated_map = {}
    cpt = 0
    for tag in map_action_tag:
        test = [tag]
        action = map_action_tag[tag]

        # Define the associated function to the tag
        if callable(action):
            action_function = action
        else:
            action_function = defined_action_map[action] if action in defined_action_map else eval(action)

        # Generate the map
        if cpt == 0:
            generated_map = generate_actions(test, action_function)
        else:
            generated_map.update(generate_actions(test, action_function))
        cpt += 1

    return generated_map


def main(defined_action_map = {}):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('input', help='Path to the input dicom file or input directory which contains dicom files')
    parser.add_argument('output', help='Path to the output dicom file or output directory which will contains dicom files')
    parser.add_argument('-t', action='append', nargs='*', help='tags action : Defines a new action to apply on the tag.'\
    '\'regexp\' action takes two arguments: '\
        '1. regexp to find substring '\
        '2. the string that will replace the previous found string')
    parser.add_argument('--dictionary', action='store', help='File which contains a dictionary that can be added to the original one')
    parser.add_argument('--keepPrivateTags', action='store_true', dest='keepPrivateTags', help='If used, then private tags won\'t be deleted')
    parser.set_defaults(keepPrivateTags=False)
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    # Create a new actions' dictionary from parameters
    new_anonymization_actions = {}
    cpt = 0
    if args.t:
        number_of_new_tags_actions = len(args.t)
        if number_of_new_tags_actions > 0:
            for i in range(number_of_new_tags_actions):
                current_tag_parameters = args.t[i]

                nb_parameters = len(current_tag_parameters)
                if nb_parameters == 0:
                    continue

                options = None
                action_name = current_tag_parameters[1]

                # Means that we are in regexp mode
                if nb_parameters == 4:
                    options = {
                        "find": current_tag_parameters[2],
                        "replace": current_tag_parameters[3]
                    }

                tags_list = [ast.literal_eval(current_tag_parameters[0])]

                action = eval(action_name)
                # When generate_actions is called and we have options, we don't want use regexp
                # as an action but we want to call it to generate a new method
                if options is not None:
                    action = action_name

                if cpt == 0:
                    new_anonymization_actions = generate_actions(tags_list, action, options)
                else:
                    new_anonymization_actions.update(generate_actions(tags_list, action, options))
                cpt += 1

    # Read an existing dictionary
    if args.dictionary:
        with open(args.dictionary) as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                action_name = value
                options = None
                if type(value) is dict:
                    action_name = value['action']
                    options = {
                        "find": value['find'],
                        "replace" : value['replace']
                    }

                l = [ast.literal_eval(key)]
                action = defined_action_map[action_name] if action_name in defined_action_map else eval(action_name)
                if cpt == 0:
                    new_anonymization_actions = generate_actions(l, action, options)
                else:
                    new_anonymization_actions.update(generate_actions(l, action, options))
                cpt += 1

    # Launch the anonymization
    anonymize(input_path, output_path, new_anonymization_actions, not args.keepPrivateTags)
