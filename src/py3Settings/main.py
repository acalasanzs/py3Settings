import json, os
from typing import Any, Callable, List
# from packages.AppSettings.utils import staticinstance

class Attribute:
    def __init__ (self, attr: str, typ : Any | None = None, validate:  Callable[[object], bool] | None = None, default: bool = False):
        self.attr = attr
        if typ is None and validate is Callable[[object], bool]:
            self.validate = validate
        elif validate is None and typ is not None:
            self.typ = typ
            self.validate = lambda a: isinstance(a, typ)
        else:
            raise SystemExit("No type!")
        self.default = default
def printObjProps(theObject):
    for property, value in vars(theObject).items():
        print(property, ":", value)
class Option():
    def __init__(self, name: str, optionName: str = "name", optionID: str | None = None):
        self.name = name
        self.optionName = optionName
        self.attributes = []
        self.default = None
        if optionID is None:
            raise SystemExit("No optionID!")
        self.optionID = optionID
    def append(self, attribute: Attribute):
        if self.default is None:
            self.default = attribute
        if attribute.default:
            self.default = attribute
        self.attributes.append(attribute)
def getWithAttr(list: list, attr: str, name: str):
    for x in list:
        if getattr(x, name) == attr:
            return x
    return False
class AppSettings():
    def __init__(self, options: List[Option]):
        self.options = options
        self.dict = dict()
        self.defaults = dict()
    def load(self, filename = "settings.json", path = os.getcwd()):
        json = AppSettings.loadJson(filename, path)
        assert isinstance(json, list)
        for i,statement in enumerate(json):
            for option in self.options:
                if option.optionName in statement and statement[option.optionName] == option.optionID:
                    for attr in statement.keys():
                        if attr in [x.attr for x in option.attributes] and not getWithAttr(option.attributes, attr, "attr").validate(statement[attr]):
                            raise SystemExit(f"Value ({statement[attr]}) [{i}] Validation Failure for {getWithAttr(option.attributes, attr, 'attr').attr} of {option.name}")
                    self.dict[option.name] = statement
                    self.defaults[option.name] = statement[option.default.attr]
    def getSetting(self, name: str, attr: str | None):
        if attr is None:
            return self.defaults[name]
        return self.dict[name][attr]
    def getSettings(self):
        return self.dict
    def getDefaultSettings(self):
        return self.defaults
    def __str__(self):
        text = ""
        for property, value in vars(self).items():
            text += " ".join([str(x) for x in [property, ":", value]])
            text += "\n"
        return text
    @staticmethod
    def loadJson(filename = "settings.json", path = os.getcwd()):
        return json.load(open(os.path.join(path,filename)))
        