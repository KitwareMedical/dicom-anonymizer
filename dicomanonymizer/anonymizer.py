import sys
if sys.version_info >= (3, 8):
    import importlib.metadata as metadata
else:
    import importlib_metadata as metadata

import argparse
import ast
import json
import os
import sys
import tqdm

from dicomanonymizer.simpledicomanonymizer import anonymize_dicom_file, ActionsMapNameFunctions


def isDICOMType(filePath):
    """
    :returns True if input file is a DICOM File. False otherwise.
    """
    try:
        with open(filePath, 'rb') as tempFile:
            tempFile.seek(0x80, os.SEEK_SET)
            return tempFile.read(4) == b'DICM'
    except IOError:
        return False


def anonymize(input_path: str, output_path: str, anonymization_actions: dict, delete_private_tags: bool) -> None:
    """
    Read data from input path (folder or file) and launch the anonymization.

    :param input_path: Path to a folder or to a file. If set to a folder,
    then cross all over sub-folders and apply anonymization.
    :param output_path: Path to a folder or to a file.
    :param anonymization_actions: List of actions that will be applied on tags.
    :param deletePrivateTags: Whether to delete private tags.
    """
    # Get input arguments
    input_folder = ''
    output_folder = ''

    if os.path.isdir(input_path):
        input_folder = input_path

    if os.path.isdir(output_path):
        output_folder = output_path
        if input_folder == '':
            output_path = os.path.join(output_folder, os.path.basename(input_path))

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
            if isDICOMType(input_folder + '/' + fileName):
                input_files_list.append(input_folder + '/' + fileName)
                output_files_list.append(output_folder + '/' + fileName)

    progress_bar = tqdm.tqdm(total=len(input_files_list))
    for cpt in range(len(input_files_list)):
        anonymize_dicom_file(input_files_list[cpt], output_files_list[cpt], anonymization_actions, delete_private_tags)
        progress_bar.update(1)

    progress_bar.close()


def parse_tag_actions_arguments(t_arguments: list, new_anonymization_actions: dict):
    """
    Parse the -t arguments and mutates the new_anonymization_actions dict

    :param t_arguments: The -t arguments as given by argparse
    :param new_anonymization_actions: The dict containing the base anonymization actions. This will be mutated.
    """
    for current_tag_parameters in t_arguments:
        nb_parameters = len(current_tag_parameters)
        if nb_parameters < 2:
            raise ValueError("-t parameters should always have 2 values: tag and action")

        tag = current_tag_parameters[0]
        action_name = current_tag_parameters[1]

        try:
            action_object = ActionsMapNameFunctions[action_name].value
        except KeyError:
            raise ValueError(f"Action {action_name} is not recognized.")

        action_arguments = current_tag_parameters[2:]

        if len(action_arguments) != action_object.number_of_expected_arguments:
            raise ValueError(f"Wrong number of arguments for action {action_name}: found {len(action_arguments)}")

        action = action_object.function if not len(action_arguments) else action_object.function(action_arguments)
        tag_list = [ast.literal_eval(tag)]

        new_anonymization_actions.update({tag: action for tag in tag_list})


def parse_dictionary_argument(dictionary_argument, new_anonymization_actions):
    """
    Parse the --dictionary argument and mutates the new_anonymization_actions dict

    :param dictionary_argument: The --dictionary argument as given by argparse
    :param new_anonymization_actions: The dict containing the base anonymization actions. This will be mutated.
    """
    with open(dictionary_argument) as json_file:
        data = json.load(json_file)
        for tag, action_or_options in data.items():
            if isinstance(action_or_options, dict):
                try:
                    action_name = action_or_options.pop('action')
                except KeyError as e:
                    raise ValueError(f"Missing field in tag {tag}: {e.args[0]}")
                try:
                    action_object = ActionsMapNameFunctions[action_name].value
                except KeyError:
                    raise ValueError(f"Action {action_name} is not recognized.")
                if len(action_or_options) != action_object.number_of_expected_arguments:
                    raise ValueError(
                        f"Wrong number of arguments for action {action_name}: found {len(action_or_options)}")
                action = action_object.function(action_or_options)
            else:
                try:
                    action = ActionsMapNameFunctions[action_or_options].value.function
                except KeyError:
                    raise ValueError(f"Action {action_or_options} is not recognized.")

            tag_list = [ast.literal_eval(tag)]
            new_anonymization_actions.update({tag: action for tag in tag_list})


def main():
    version_info = metadata.version("dicom_anonymizer")
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('input', help='Path to the input dicom file or input directory which contains dicom files')
    parser.add_argument(
        'output', help='Path to the output dicom file or output directory which will contains dicom files')
    parser.add_argument(
        '-t', action='append', nargs='*',
        help='tags action : Defines a new action to apply on the tag.\'regexp\' action takes two arguments: '
        '1. regexp to find substring 2. the string that will replace the previous found string')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {version_info}')
    parser.add_argument('--dictionary', action='store',
                        help='File which contains a dictionary that can be added to the original one')
    parser.add_argument('--keepPrivateTags', action='store_true', dest='keepPrivateTags',
                        help='If used, then private tags won\'t be deleted')
    parser.set_defaults(keepPrivateTags=False)
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    # Create a new actions' dictionary from parameters
    new_anonymization_actions = {}
    if args.t:
        parse_tag_actions_arguments(args.t, new_anonymization_actions)

    # Read an existing dictionary
    if args.dictionary:
        parse_dictionary_argument(args.dictionary, new_anonymization_actions)

    # Launch the anonymization
    anonymize(input_path, output_path, new_anonymization_actions, not args.keepPrivateTags)


if __name__ == '__main__':
    main()
