"""
BEGIN
Path replacement
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
"""
END
Path replacement
"""