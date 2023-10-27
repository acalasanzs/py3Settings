from setdir import get_path, get
tests = get("child","tests", 1)
# tests = get_path("tests")
print(tests)
import sys, os
sys.path.append(r'C:\Users\acses\Documents\py3Settings\src\py3Settings')
from main import AppSettings, Option, Attribute
from typing import List