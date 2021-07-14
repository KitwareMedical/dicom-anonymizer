from typing import Union
from pathlib import Path

# Type defs
Path_Str = Union[str, Path]


def to_Path(p: Path_Str):
    """Convert str to Path

    Args:
        p (Path_Str): path

    Raises:
        TypeError: in case not a valid type for Path

    Returns:
        [Path]: path
    """
    try:
        return Path(p)
    except TypeError:
        raise TypeError(f"Invalid type of {p}")


def create_if_not_exist(path: Path, **kwargs):
    """Helper to make sure path exists

    Args:
        path (Path): path to create if not exists
    """
    if not path.exists():
        path.mkdir(**kwargs)


def try_valid_path(path: Path):
    """Raise error if path doesn't exist

    Args:
        path (Path): path to check

    Raises:
        FileExistsError: if not exist
    """
    if not path.exists():
        raise FileExistsError


def try_valid_dir(path: Path):
    """Raising if not exists or not a directory

    Args:
        path (Path): path to check

    Raises:
        NotADirectoryError:
    """
    try_valid_path(path)
    if not path.is_dir():
        raise NotADirectoryError


def get_dirs(root_path: Path):
    """Finds all folders in the root recursivly

    Args:
        root_path (Path): root path

    Yields:
        Path: directory inside the root path
    """
    for p in root_path.iterdir():
        if p.is_dir():
            yield p
            yield from get_dirs(p)
