from main import AppSettings, Option, Attribute
from typing import List
import os
# options: List[Option] = list()
# content = Option("content","warn","Already with content in it!")
# content.append(Attribute("ask", bool))
# exists = Option("exists","warn","{x} already exists!")
# exists.append(Attribute("ask", bool))
# settingsProxy = AppSettings([content,exists])
# settingsProxy.loadFile("sure.json", os.path.abspath(os.path.join(__file__,'..','..','..','tests')))
# print(settingsProxy)
# settingsProxy.saveFile('algo.json', os.path.abspath(os.path.join(__file__,'..','..','..','tests')))
# settingsProxy.validateAll()


# Recursividad
options: List[Option] = list()
for x in range(3):
    x = Option(str(x), "set", f"Parameter {x}")
    x.append(Attribute)