import os
from typing import Any, Callable, Iterator, List
import file
from proxy import *
from utils import *
from collections.abc import Mapping
import uuid
from modules import *
# from packages.AppSettings.utils import staticinstance
class Option:
    """_summary_
    In the Option class, optionID is a unique identifier for the option, while optionName is the name of the option. The optionID is used to differentiate between different options, while the optionName is used to identify the option in the settings data.
    """

    def __init__(
        self, name: str, optionName: str = "name", attributes: ['Attribute | InAttribute'] = []
    ):
        self.name = name
        self.optionName = optionName
        self.attributes = []
        self.default = None
        for x in attributes:
            self.append(x)

    def append(self, attribute: 'Attribute | InAttribute'):
        if self.default is None:
            self.default = attribute
        if type(attribute) is Attribute and attribute.default:
            self.default = attribute
        self.attributes.append(attribute)
        return
class InAttribute:

    def __init__(self, attr: str, options: List[Option], validateAll: bool = True):
        self.attr = attr
        self.validateAll = validateAll
        self.options = AppSettings(options)
formats = [handle(".json", file.JSON)]


def addFormatSupport(Handler: Handler):
    formats.append(Handler)


def showFileDefs():
    return file

class AppSettings(Mapping):
    """_copilot-suggerence_     
    def to_dict(self, nested=False):
            data = {}
            for option in self.options:
                value = self.dict[option.name]
                for attr in option.attributes + option.inAttributes:
                    if isinstance(value[attr.attr], AppSettings):
                        value[attr.attr] = value[attr.attr].to_dict(nested=True)
                    elif callable(value[attr.attr]):
                        value[attr.attr] = value[attr.attr]()
                    elif isinstance(value[attr.attr], Mapping):
                        value[attr.attr] = dict(value[attr.attr])
                data[option.name] = value
            if nested:
                return data
            else:
                return AppSettings.preProcess(data)

        @classmethod
        def from_dict(cls, data):
            options = []
            for key in data:
                # Generate a random UUID
                random_uuid = uuid.uuid4()
                random = Option(f"import_{random_uuid}", key, data[key])
                if has_nested_object(data[key]):
                    for sub_key in data[key]:
                        if isinstance(data[key][sub_key], dict):
                            random.append(InAttribute(sub_key, [Attribute("attr", type(data[key][sub_key][sub_sub_key]), default=data[key][sub_key][sub_sub_key]) for sub_sub_key in data[key][sub_key]]))
                        else:
                            random.append(Attribute(sub_key, type(data[key][sub_key]), default=data[key][sub_key]))
                options.append(random)
            return AppSettings(options) 
    """

    def __init__(self, options: List[Option]):
        self.options = options
        self.dict = dict()
        self.defaults = dict()
        self.i = 0
        self.putAll = False

    def __getitem__(self, __key: str | int) -> Option:
        for i, x in enumerate(self.options):
            if __key == x.name or i == __key:
                return x

    def __delitem__(self, __key: str | int) -> None:
        for i, x in enumerate(self.options):
            if __key == x.name or i == __key:
                self.options.remove(x)
                return

    def __iter__(self):
        return self

    def __len__(self) -> int:
        return self.options.__len__()

    def __next__(self):
        if self.__len__() == self.i:
            raise StopIteration
        x = self.options[self.i]
        self.i += 1
        return x

    @staticmethod
    def _loadFile(filename: str, path=os.getcwd()):
        type = "." + filename.split(".")[1]
        for x in formats:
            if x.format == type:
                if len(filename) == 0:
                    filename = f"settings{x.format}"
                return x.load(filename, path)
        return False

    @staticmethod
    def _saveFile(data: list, filename: str, path=os.getcwd()):
        type = "." + filename.split(".")[1]
        for x in formats:
            if x.format == type:
                if len(filename) == 0:
                    filename = f"settings{x.format}"
                return x.save(data, filename=filename, path=path)
        return False

    def loadFile(self, *args, **kwargs):
        data = AppSettings._loadFile(*args, **kwargs)
        if data is False:
            raise SystemExit("Format not supported")
        return self.load(data)

    def saveFile(self, *args, **kwargs):
        return AppSettings._saveFile(self.preload(), *args, **kwargs)
    def preload(self):
        all = []
        for option in self.options:
            written = self.retrieve(option, self.dict)
            actual = self.retrieve(option, self.defaults)
            if written is not None:
                written = written['plain']
            if actual is not None:
                actual = actual['plain']
            if written is not None:
                for key, value in written.items():
                    if type(value) is AppSettings:
                        written[key] = value.preload()[0]
                all.append(written)
            if self.putAll and actual is not None:
                all.append(actual)
        return all
    def retrieve(self, option, where):
        """_summary_
                    This method searches all over self.dict and self.defaults so it can get the direct match about that option, so it can be retrieved for validating it to the current attribute.
                Args:
                    option (Option): The option is going to be used as the match indicator
                    
        """
        for key in where.keys():
            if key == option.name:
                attrs = where[key].keys()
                return {
                    "native": option.attributes,
                    "plain": where[key]
                }
    def searchMatch(self, option):
            sdict = self.retrieve(option, self.dict)
            if sdict is not None:
                for sd in sdict['plain']:
                    attr = getWithAttr(sdict['native'], sd, "attr")
                    if type(attr) is Attribute:
                        attr.validate(sdict['plain'][sd])
                    elif type(attr) is InAttribute:
                        attr.options.validateAll()
                if len(option.attributes) > len(sdict['plain']):
                    new = []
                    for x in option.attributes:
                        if type(x) is InAttribute:
                            new.append(x)
                    return new
            return False
    def validateAll(self):
        i = 0          
            

        # Only validates the ones that are neither default or undefined, which is only self.dict
        for key, value in self.dict.items():
            # For all the options that meet the above requirements
            for option in self.options:
                
                option_class = self.searchMatch(option)
                if option_class:
                    for app in option_class:
                        app.options.validateAll()
                    
            i += 1
        return f"validated {i} attributes of options"
    def load(self, data: list):
        assert isinstance(data, list)
        for i, statement in enumerate(data):
            for option in self.options:
                if (
                    option.optionName in statement
                ):
                    for attr in [
                        y for y in list(statement.keys()) if y != option.optionName
                    ]:
                        attr_get = getWithAttr(option.attributes, attr, "attr")
                        val = attr_get.validate(statement[attr])
                        if attr in [x.attr for x in option.attributes] and not val:
                            raise SystemExit(
                                f"Value ({statement[attr]}) [{i}] Validation Failure for {attr_get.attr} of {option.name}"
                            )
                        if callable(val):
                            statement[attr] = val()
                    self.dict[option.name] = statement                                             #  Where the dict or defaults changes                  ###################################################################
                    self.defaults[option.name] = statement[option.default.attr]
                    if type(option.default) is InAttribute:
                        self.defaults[option.name] = option.default

    def getSetting(self, name: str, attr: str | None):
        def getSettingClosure():
            value = getWithAttr(self.options, name, "name")
            if value is not None:
                try:
                    return self.dict[value.name][attr]
                except KeyError:
                    self.defaults[option.name] = specialDict(option.default.attr, option.default.default)
                    return value.default.default
            else:
                return self.defaults[name][attr].get(self.defaults[attr])
        def getAppClosure():
            value = getWithAttr(self.options, name, "name")
            if value is not None:
                return getWithAttr(value.attributes, attr, "attr").options
            else:
                return self.defaults[name][attr].get(self.defaults[attr])
        if attr is None:
            return getSettingClosure(self.defaults[name])
        # try:
        option = next((option for option in self.options if option.name == name), None)
        if option is None:
            raise KeyError(f"Option {name} not found in settings")

        attr_get = getWithAttr(option.attributes, attr, "attr")
        if attr_get is None:
            raise KeyError(f"Attribute {attr} not found in {option.name}")

        if isinstance(attr_get, InAttribute):
            return getAppClosure()
        else:
            return getSettingClosure()
        # except KeyError:
        #     raise KeyError(f"Attribute {attr} not found in settings")

    def getSettings(self):
        all = {
            "native": [],
            "plain": []
        }
        for option in self.options:
            sdict = self.retrieve(option, self.dict)
            sdef = self.retrieve(option, self.defaults)
            if sdict['native'] is not None:
                all['native'].append(sdict['native'])
            else:
                all['native'].append(sdef['native'])
            if sdict['plain'] is not None:
                all['plain'].append(sdict['plain'])
            else:
                all['plain'].append(sdef['plain'])
        return all
    
    def writeSetting(self, name: str, attr: str, value: Any):
        if self.dict.get(name) is None:
            self.dict[name] = specialDict(attr, value)
            return
        self.dict[name][attr] = value
    def pushSetting(self, name: str, attr: str, innerDefault: bool = False):
        self.validateAll()
        value = [x for x in getWithAttr(self.options, name, "name").attributes if x.attr == attr]
        if len(value) == 0:
            return
        value = value[0]
        try:
            self.dict.pop(name, None)
            self.defaults.pop(name, None)
        except:
            self.defaults.pop(name, None)
        if type(value) is InAttribute:
            where = self.defaults if innerDefault else self.dict
            if where.get(name) is None:
                where[name] = specialDict(value.attr, value.options)
            else:
                where[name][value.attr] = value.options
        elif type(value) is Attribute:
            if self.defaults.get(name) is None:
                self.defaults[name] = specialDict(value.attr, value.default)
            else:
                self.defaults[name][value.attr] = value.default
    def getDefaultSettings(self):
        return self.defaults

    def __str__(self):
        text = ""
        for property, value in vars(self).items():
            text += " ".join([str(x) for x in [property, ":", value]])
            text += "\n"
        return text
