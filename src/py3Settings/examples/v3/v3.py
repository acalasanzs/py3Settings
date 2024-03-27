from setdir import get_path, get
from copy import deepcopy as dc
tests = get("child","tests", 1)
# tests = get_path("tests")
print(tests)
import sys, os
# sys.path.append(r'C:\Users\acses\Documents\py3Settings\src\py3Settings')
# from main import AppSettings, Option, Attribute
from main import InAttribute, AppSettings, Option, Attribute
from typing import List
# Example usage3
attr1 = Attribute("attr1", validate= lambda x: x > 0)
attr2 = Attribute("attr2", validate=lambda x: len(x) > 0, default="default_value")
inAttr = InAttribute("inAttr", [Option("sub_option",None, dc([attr1, attr2]))])
my_option = Option("my_option", "option_id")
my_second_option = Option("another", "whatItTalksInside")
my_option.append(attr1)
my_second_option.append(inAttr)

my_settings = AppSettings([my_option, my_second_option])
all = my_settings
# my_settings.validateAll()
# Set values for attributes.
print(all)

# my_settings.writeSetting("my_option", "attr1", 2)
my_settings.writeSetting("my_option", "attr2", "new_value")

# Validate all attributes: IF ANY FAILS, IT WILL RAISE AN ERROR.
print(my_settings.getSetting("my_option", "attr1"))  # Output: 2

# Get value of attribute

# Get values of InAttribute object

#Instead, write from origin to replace default
sub_app = my_settings.getSetting("another", "inAttr")
sub_app.writeSetting("sub_option", "attr1", "Albert")
all.pushSetting("another", "inAttr")
# all.putAll = True
print("pass 2")
# print(my_settings.getSetting("my_option", "inAttr"))  # Output: {'attr1': 2, 'attr2': 'new_value'}
"""reality:
    options : [<main.Option object at 0x00000275346F9640>]
    dict : {}
    defaults : {}
    i : 0
"""
my_settings.saveFile(r"C:\Users\acses\Documents\py3Settings\tests\algov3.json", tests)
print("ok")