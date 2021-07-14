""" This module is intended to extend functionality of the code provided by original authors.
    The process is as follows:
    1. User has to provide source root path containing (possibly nested) folders with dicom files
    2. The program will recreate the structure in the destination root path and anonymize all
    dicom files.
"""

import argparse
import json
import random
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

_STATE_PATH = Path.home() / ".dicomanonymizer/cache"
create_if_not_exist(_STATE_PATH, parents=True)
STATE_FILE = _STATE_PATH / "state_cache.json"


def anonymize_dicom_folder(in_path: Path_Str, out_path: Path_Str, debug: bool = False):
    """Anonymize dicom files in `in_path`, if `in_path` doesn't
    contain dicom files, will do nothing. Debug == True will do
    sort of dry run to check if all good for the large data storages

    Args:
        in_path (Path_Str): path to the folder containing dicom files
        out_path (Path_Str): path to the folder there anonymized copies
        will be saved
        debuf (bool): if true, will do a "dry" run
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

    if debug:
        # anonymize just one file
        f_in = random.choice(in_files)
        f_out = out_path / f_in.name
        anonymize_dicom_file(f_in, f_out)
    else:
        for f_in in in_files:
            f_out = out_path / f_in.name
            anonymize_dicom_file(f_in, f_out)


def anonymize_root_folder(in_root: Path_Str, out_root: Path_Str, **kwargs):
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

    try:
        with open(STATE_FILE, "r") as f:
            processed_state = json.load(f)
    except FileNotFoundError:
        processed_state = None
    if processed_state is None:
        processed_state = {}

    # will try to process all folders, if exception will dump state before raising
    try:
        for in_d in in_dirs:
            if str(in_d) in processed_state:
                continue
            else:
                rel_path = in_d.relative_to(in_root)
                out_d = out_root / rel_path
                anonymize_dicom_folder(in_d, out_d, **kwargs)
                # update state
                processed_state[str(in_d)] = str(out_d)
    except Exception as e:
        raise e
    finally:
        with open(STATE_FILE, "w") as f:
            json.dump(processed_state, f)


# Add CLI args
parser = argparse.ArgumentParser(description="Batch dicom-anonymization CLI")
parser.add_argument(
    "--type",
    type=str,
    choices=["batch", "folder"],
    default="batch",
    help="Process only one folder - folder or all nested folders - batch, default = batch",
)
parser.add_argument(
    "--debug", action="store_true", help="Will do a dry run (one file per folder)"
)
parser.add_argument(
    "src",
    type=str,
    help="Absolute path to the folder containing dicom-files or nested folders with dicom-files",
)
parser.add_argument(
    "dst",
    type=str,
    help="Absolute path to the folder where to save anonymized copy of src",
)


def main():
    args = parser.parse_args()
    in_path = Path(args.src)
    out_path = Path(args.dst)
    debug = args.debug
    # fix known issue with dicom
    fix_exposure()
    if args.type == "batch":
        anonymize_root_folder(in_path, out_path, debug=debug)
    elif args.type == "folder":
        anonymize_dicom_folder(in_path, out_path, debug=debug)


if __name__ == "__main__":
    main()
