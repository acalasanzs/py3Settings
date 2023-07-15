import os
from typing import Any, Callable, List
import py3Settings
from py3Settings import file
from py3Settings.proxy import *
# from packages.AppSettings.utils import staticinstance
class Attribute:
    def __init__ (self, attr: str, typ : Any | None = None, validate:  Callable[[object], bool] | None = None, default: bool = False, getter: Callable[[], Any] = None):
        self.attr = attr
        if typ is None and validate is Callable[[object], bool]:
            self.validate = validate
        elif validate is None and typ is not None:
            self.typ = typ
            self.validate = lambda a: isinstance(a, typ) if not hasattr(self, 'get') else self.get
            if getter is not None:
                self.get = getter
        else:
            raise SystemExit("No type!")
        self.default = default
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
formats = [handle('.json',file.JSON)]

def addFormatSupport(Handler: Handler):
    formats.append(Handler)
def showFileDefs():
    return file
class AppSettings():
    def __init__(self, options: List[Option]):
        self.options = options
        self.dict = dict()
        self.defaults = dict()
    @staticmethod
    def _loadFile(filename:str, path = os.getcwd()):
        type = "."+filename.split(".")[1]
        for x in formats:
            if x.format == type:
                if(len(filename) == 0):
                    filename = f"settings{x.format}"
                return x.load(filename, path)
        return False
    @staticmethod
    def _saveFile(data: list, filename:str, path = os.getcwd()):
        type = "."+filename.split(".")[1]
        for x in formats:
            if x.format == type:
                if(len(filename) == 0):
                    filename = f"settings{x.format}"
                return x.save(data, filename = filename, path = path)
        return False
    def loadFile(self, *args,**kwargs):
        data = AppSettings._loadFile(*args,**kwargs)
        if data is False:
            raise SystemExit("Format not supported")
        return self.load(data)
    def saveFile(self, *args,**kwargs):
        return AppSettings._saveFile(AppSettings.preProcess(self.dict), *args,**kwargs)
    @staticmethod
    def preProcess(data: dict):
        return [x for x in data.values()]
    def validateAll(self):
        i = 0
        for key, value in self.dict.items():
            for option in self.options:
                if option.optionName in value and value[option.optionName] == option.optionID:
                    for attr in [y for y in list(value.keys()) if y != option.optionName]:
                        attr_get = getWithAttr(option.attributes, attr, 'attr')
                        val = attr_get.validate(value[attr])
                        if attr in [x.attr for x in option.attributes] and not val:
                            raise SystemExit(f"Value ({value[attr]}) [{i}] Validation Failure for {attr_get.attr} of {option.name}")
                        if callable(val):
                            value[attr] = val()
                    self.dict[option.name] = value
                    self.defaults[option.name] = value[option.default.attr]
            i += 1
    def load(self, data: list):
        assert isinstance(data, list)
        for i,statement in enumerate(data):
            for option in self.options:
                if option.optionName in statement and statement[option.optionName] == option.optionID:
                    for attr in [y for y in list(statement.keys()) if y != option.optionName]:
                        attr_get = getWithAttr(option.attributes, attr, 'attr')
                        val = attr_get.validate(statement[attr])
                        if attr in [x.attr for x in option.attributes] and not val:
                            raise SystemExit(f"Value ({statement[attr]}) [{i}] Validation Failure for {attr_get.attr} of {option.name}")
                        if callable(val):
                            statement[attr] = val()
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
        