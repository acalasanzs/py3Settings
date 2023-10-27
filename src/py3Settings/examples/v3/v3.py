from setdir import get_path, get
tests = get("child","tests", 1)
# tests = get_path("tests")
print(tests)
import sys, os
sys.path.append(r'C:\Users\acses\Documents\py3Settings\src\py3Settings')
# from main import AppSettings, Option, Attribute
from main import InAttribute, AppSettings, Option, Attribute
from typing import List
# Example usage
attr1 = Attribute("attr1", lambda x: x > 0, default=1)
attr2 = Attribute("attr2", lambda x: len(x) > 0, default="default_value")
inAttr = InAttribute("inAttr", [attr1, attr2])
my_option = Option("my_option", "option_id")
my_option.append(attr1)
my_option.append(inAttr)

my_settings = AppSettings([my_option])

# Set values for attributes
my_settings.writeSetting("my_option", "attr1", 2)
my_settings.writeSetting("my_option", "attr2", "new_value")

# Validate all attributes
my_settings.validateAll()

# Get value of attribute
print(my_settings.getSetting("my_option", "attr1"))  # Output: 2

# Get values of InAttribute object
print(my_settings.getSetting("my_option", "inAttr"))  # Output: {'attr1': 2, 'attr2': 'new_value'}
my_settings.saveFile(r"C:\Users\acses\Documents\py3Settings\tests\algov3.json", tests)