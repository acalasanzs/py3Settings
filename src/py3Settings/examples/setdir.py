"""
This script sets the working directory and adds it to the system path. It reads the parent directory level from a file called 'innerdir' located in the same directory as this script. The parent directory level is used to determine the working directory by going up the directory tree by the specified number of levels. It also sets the 'tests' directory path as an absolute path by going up two directory levels from the working directory.

Usage: 
    python setdir.py

Example:
    If the 'innerdir' file contains 'parent,2', then the working directory will be set to the grandparent directory of this script and the 'tests' directory path will be set to the absolute path of the 'tests' directory located in the grandparent directory.

"""
import sys
import os.path
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
parent = 0
with open(os.path.join(__location__,"innerdir")) as innerdir:
    opt = innerdir.read().split(",")
    assert opt[0] == "parent"
    parent = int(opt[1])
    del opt
workdir = os.path.abspath(os.path.join(os.path.dirname(__file__), *[os.path.pardir for _ in range(parent)]))
tests = os.path.abspath(os.path.join(workdir, *[os.path.pardir for _ in range(2)], 'tests'))
sys.path.append(workdir)
