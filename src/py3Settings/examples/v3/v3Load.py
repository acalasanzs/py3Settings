from setdir import get_path, get
from copy import deepcopy as dc
tests = get("child","tests", 1)
# tests = get_path("tests")
print(tests)
# import sys, os
# sys.path.append(r'C:\Users\acses\Documents\py3Settings\src\py3Settings')
# from main import AppSettings, Option, Attribute
from py3Settings import InAttribute, AppSettings, Option, Attribute
from typing import List

def setup():
# Example usage3
    attr1 = Attribute("attr1", validate=lambda x: x > 0, default=1)
    attr2 = Attribute("attr2", validate=lambda x: len(x) > 0, default="default_value")
    inAttr = InAttribute("inAttr", [Option("sub_option", dc([attr1, attr2]))])
    my_option = Option("my_option")
    my_second_option = Option("another")
    my_option.append(attr1)
    my_second_option.append(inAttr)

    my_settings = AppSettings([my_option, my_second_option])
    return my_settings

all = setup()
all.loadFile(r"C:\Users\acses\Documents\py3Settings\tests\surev3.json", tests)
all.saveFile(r"C:\Users\acses\Documents\py3Settings\tests\algov3.json", tests)
print("ok")