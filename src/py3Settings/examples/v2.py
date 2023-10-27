from init import *

options: List[Option] = list()
content = Option("content", "warn")
content.append(Attribute("ask", bool))
content.append(Attribute("name", str))
exists = Option("exists", "warn")
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
