import os
from typing import Any, Callable, List
from . import file
# from packages.AppSettings.utils import staticinstance
import re
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
def handle(format, dict:dict):
    ins = Handler(format)
    ins.init(**dict)
    return ins
class Handler:
    invalid = r'[<>:"/\|?* ]'
    def __init__(self, format: str):
        self.format = format
    def init(self, load: Callable[[str,str], dict], save: Callable[[dict], str | bool]):
        self.load = Handler.safeCheck(load)
        self.save = Handler.safeCheck(save)
    @staticmethod
    def safeCheck(fun):
        def wrapper(*args, **kwargs):
            assert Handler.fileStr(kwargs.get('filename') or args[0])
            return fun(*args, **kwargs)
        return wrapper
    @classmethod
    def fileStr(cls, file: str) -> bool:
        file = file.split(".")
        if(len(file) != 2):
            return False
        filename = file[0]
        original = file[0]
        if re.search(cls.invalid, filename):
            return False
        if original != filename:
            return False
        return True
formats = [handle('.json',file.JSON)]
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
        