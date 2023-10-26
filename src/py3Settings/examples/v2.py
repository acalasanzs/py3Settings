from setdir import tests
print(tests)
from main import AppSettings, Option, Attribute
from typing import List

options: List[Option] = list()
content = Option("content", "warn", "Already with content in it!")
content.append(Attribute("ask", bool))
exists = Option("exists", "warn", "{x} already exists!")
exists.append(Attribute("ask", bool))
settingsProxy = AppSettings([content, exists])
settingsProxy.loadFile("sure.json", tests)
print(settingsProxy)
settingsProxy.saveFile("algo.json", tests)
settingsProxy.validateAll()
print("\n\n\n---")
for x in settingsProxy:
    print(x)
print(settingsProxy["exists"])
print(settingsProxy[1])
