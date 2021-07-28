""" This module is intended to extend functionality of the code provided by original authors.
    The process is as follows:
    1. User has to provide source root path containing (possibly nested) folders with dicom files
    2. The program will recreate the structure in the destination root path and anonymize all
    dicom files.
"""

import argparse
import logging
import logging.config
import random
from pathlib import Path

import pydicom

from dicomanonymizer.anonym_state import AnonState
from dicomanonymizer.dicom_utils import fix_exposure
from dicomanonymizer.simpledicomanonymizer import anonymize_dicom_file
from dicomanonymizer.utils import (
    LOGS_PATH,
    PROJ_ROOT,
    Path_Str,
    create_if_not_exist,
    get_dirs,
    to_Path,
    try_valid_dir,
)

# setup logging (create dirs, if it is first time)
create_if_not_exist(LOGS_PATH, parents=True, exist_ok=True)
logging.config.fileConfig(
    PROJ_ROOT / "dicomanonymizer/config/logging.ini",
    defaults={"logfilename": (LOGS_PATH / "file.log").as_posix()},
    disable_existing_loggers=False,
)
logger = logging.getLogger(__name__)

_STATE_PATH = Path.home() / ".dicomanonymizer/cache"
create_if_not_exist(_STATE_PATH, parents=True)


def anonymize_dicom_folder(
    in_path: Path_Str, out_path: Path_Str, debug: bool = False, **kwargs
):
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

    logger.info(f"Processing: {in_path}")
    # work itself
    in_files = [p for p in in_path.iterdir() if p.is_file()]

    if not in_files:
        logger.info(f"Folder {in_path} doesn't have dicom files, skip.")
        return

    if debug:
        # anonymize just one file
        f_in = random.choice(in_files)
        f_out = out_path / f_in.name
        try:
            anonymize_dicom_file(f_in, f_out)
        except Exception as e:
            logger.info(f_in)
            logger.exception(e)
            raise e
    else:
        for f_in in in_files:
            f_out = out_path / f_in.name
            try:
                anonymize_dicom_file(f_in, f_out, **kwargs)
            except Exception as e:
                logger.info(f_in)
                logger.exception(e)
                raise e


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

    state = AnonState(_STATE_PATH)
    state.init_state()
    state.load_state()

    def get_tags_callback(dataset: pydicom.Dataset):
        state.tag_counter.update(dataset.dir())

    logger.info(
        "Processed paths will be added to the cache, if cache exist and has some paths included, they will be skipped"
    )
    logger.info(
        f"if, you need to process data again delete files {_STATE_PATH}, please"
    )

    # will try to process all folders, if exception will dump state before raising
    try:
        for in_d in in_dirs:
            rel_path = in_d.relative_to(in_root)
            if str(rel_path) in state.visited_folders:
                logger.info(f"{in_d} path is in cache, skipping")
                continue
            else:
                out_d = out_root / rel_path
                anonymize_dicom_folder(
                    in_d, out_d, ds_callback=get_tags_callback, **kwargs
                )
                # update state
                state.visited_folders[str(rel_path)] = True
    except Exception as e:
        raise e
    finally:
        # before saving updated state let's flag tags not seen previously
        prev_state = AnonState(_STATE_PATH)
        prev_state.init_state()
        prev_state.load_state()
        new_tags = set(state.tag_counter.keys()).difference(
            prev_state.tag_counter.keys()
        )
        if new_tags:
            logger.warning(
                f"During the anonymization new tags: {new_tags} were present"
            )
        else:
            logger.info("No new tags werer present")
        # now we can save the current state
        state.save_state()


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
    # parse args
    args = parser.parse_args()
    in_path = Path(args.src)
    out_path = Path(args.dst)
    debug = args.debug
    # fix known issue with dicom
    fix_exposure()
    msg = f"""
    Start a job: {args.type}, debug set to {args.debug}
    Will anonymize data at: {in_path} and save to {out_path}
    """
    logger.info(msg)
    # anonymize
    if args.type == "batch":
        anonymize_root_folder(in_path, out_path, debug=debug)
    elif args.type == "folder":
        anonymize_dicom_folder(in_path, out_path, debug=debug)
    logger.info("Well done!")


if __name__ == "__main__":
    main()
