""" This module is intended to extend functionality of the code provided by original authors.
    The process is as follows:
    1. User has to provide source root path containing (possibly nested) folders with dicom files
    2. The program will recreate the structure in the destination root path and anonymize all
    dicom files.
"""

import argparse
from pathlib import Path

from dicomanonymizer.dicom_utils import fix_exposure
from dicomanonymizer.simpledicomanonymizer import anonymize_dicom_file
from dicomanonymizer.utils import (
    Path_Str,
    create_if_not_exist,
    get_dirs,
    to_Path,
    try_valid_dir,
)


def anonymize_dicom_folder(in_path: Path_Str, out_path: Path_Str):
    """Anonymize dicom files in `in_path`, if `in_path` doesn't
    contain dicom files, will do nothing

    Args:
        in_path (Path_Str): path to the folder containing dicom files
        out_path (Path_Str): path to the folder there anonymized copies
        will be saved
    """
    # check and prepare
    in_path = to_Path(in_path)
    try_valid_dir(in_path)

    out_path = to_Path(out_path)
    create_if_not_exist(out_path)

    print(f"Processing: {in_path}")
    # work itself
    in_files = [p for p in in_path.iterdir() if p.is_file()]

    if not in_files:
        print(f"Folder {in_path} doesn't have dicom files, skip.")
        return

    for f_in in in_files:
        f_out = out_path / f_in.name
        anonymize_dicom_file(f_in, f_out)


def anonymize_root_folder(in_root: Path_Str, out_root: Path_Str):
    """The fuction will get all nested folders from `in_root`
    and perform anonymization of all folders containg dicom-files
    Will recreate the `in_root` folders structure in the `out_root`

    Args:
        in_root (Path_Str): source root folder (presumably has
        some dicom-files inide, maybe nested)
        out_root (Path_Str): destination root folder, will create
        if not exists
    """
    in_root = to_Path(in_root)
    try_valid_dir(in_root)
    out_root = to_Path(out_root)
    create_if_not_exist(out_root)
    in_dirs = get_dirs(in_root)

    for in_d in in_dirs:
        rel_path = in_d.relative_to(in_root)
        out_d = out_root / rel_path
        anonymize_dicom_folder(in_d, out_d)


# Add CLI args
parser = argparse.ArgumentParser(description="Batch dicom-anonymization CLI")
parser.add_argument(
    "--type",
    type=str,
    required=True,
    choices=["batch", "folder"],
    help="Process only one folder or all nested folders",
)
parser.add_argument(
    "--src",
    type=str,
    required=True,
    help="Absolute path to the folder containing dicom-files or nested folders with dicom-files",
)
parser.add_argument(
    "--dst",
    type=str,
    required=True,
    help="Absolute path to the folder where to save anonymized copy of src",
)


def main():
    args = parser.parse_args()
    in_path = Path(args.src)
    out_path = Path(args.dst)
    # fix known issue with dicom
    fix_exposure()
    if args.type == "batch":
        anonymize_root_folder(in_path, out_path)
    elif args.type == "folder":
        anonymize_dicom_folder(in_path, out_path)


if __name__ == "__main__":
    main()
