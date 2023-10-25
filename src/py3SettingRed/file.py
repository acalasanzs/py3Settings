import json, os
def loadJson(filename = "settings.json", path = os.getcwd()):
    return json.load(open(os.path.join(path,filename)))
def saveJson(data: dict, filename = "settings.json", path = os.getcwd()):
    with open(os.path.join(path,filename), 'w') as fp:
        json.dump(data, fp)
JSON = {
    "load": loadJson,
    "save": saveJson
}