"""
BEGIN
Path replacement
"""
import sys
import os.path
from functools import partial
import pathlib
# this_module = sys.modules[__name__]
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

import os
import sys

def get_targetFolder(targetFolder: str = 'tests', dirsFromParent: int = 2):
    """
    Returns the absolute path of the target folder, which is located a specified number of directories away from the parent directory.

    Args:
        targetFolder (str): The name of the target folder. Defaults to 'tests'.
        dirsFromParent (int): The number of directories away from the parent directory where the target folder is located. Defaults to 2.

    Returns:
        str: The absolute path of the target folder.
    """
    parent = 0
    with open(os.path.join(__location__,"innerdir")) as innerdir:
        opt = innerdir.read().split(",")
        assert opt[0] == "parent"
        parent = int(opt[1])
        del opt
    workdir = os.path.abspath(os.path.join(os.path.dirname(__file__), *[os.path.pardir for _ in range(parent)]))
    tests = os.path.abspath(os.path.join(workdir, *[os.path.pardir for _ in range(dirsFromParent)], targetFolder))
    sys.path.append(workdir)
def setLocationRef(targetFolder: str = 'tests', dirsFromParent: int = 2):
    return partial(get_targetFolder,targetFolder,dirsFromParent )
def setAbsoluteRefTree(path: str, targetFolder: str = 'tests', dirsFromParent: int = 2):
    path = pathlib.Path(path)
    if not path.exists():
        raise FileNotFoundError
    if path.is_file():
        warning

"""
END
Path replacement
"""