from setdir import get_path, get
tests = get("child","tests", 1)
# tests = get_path("tests")
print(tests)
import sys, os
sys.path.append(r'C:\Users\acses\Documents\py3Settings\src\py3Settings')
from main import AppSettings, Option, Attribute
from typing import List

options: List[Option] = list()
content = Option("content", "warn", "Already with content in it!")
content.append(Attribute("ask", bool))
content.append(Attribute("name", str))
exists = Option("exists", "warn", "{x} already exists!")
exists.append(Attribute("ask", bool))
settingsProxy = AppSettings([content, exists])
settingsProxy.loadFile(r"C:\Users\acses\Documents\py3Settings\tests\sure.json", tests)
print(settingsProxy)
settingsProxy.saveFile(r"C:\Users\acses\Documents\py3Settings\tests\algo.json", tests)
settingsProxy.validateAll()
print("\n\n\n---")
for x in settingsProxy:
    print(x)
print(settingsProxy["exists"])
print(settingsProxy[1])
