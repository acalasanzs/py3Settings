import os
from typing import Any, Callable, Iterator, List
import file
from proxy import *
from utils import *
from collections.abc import Mapping
import uuid

# from packages.AppSettings.utils import staticinstance
class Attribute:
    """example:
    ```python
            Define an attribute for the option
            attr1 = Attribute("attr1", int, lambda x: x > 0, default=1)

            Define another attribute for the option
            attr2 = Attribute("attr2", str, lambda x: len(x) > 0, default="default_value")

            Create an option with the attributes
            my_option = Option("my_option", "option_id")
            my_option.append(attr1)
            my_option.append(attr2)```
    
        In this example, we define an Attribute called attr1 with a name of "attr1", a type of int, a validation function that checks if the value is greater than 0, and a default value of 1. We also define another Attribute called attr2 with a name of "attr2", a type of str, a validation function that checks if the length of the value is greater than 0, and a default value of "default_value".

        We then create an Option called my_option with an option name of "my_option", an option ID of "option_id", and append the attr1 and attr2 attributes to it.

        This Option now has two attributes that can be used to validate and process data in the AppSettings class. For example, if we have a settings file with a "my_option" section that contains "attr1" and "attr2" keys, we can use the validateAll method of the AppSettings class to validate the values of these keys using the attr1 and attr2 attributes of the my_option option.
    parameters:
        self: A reference to the instance of the class being created.
        
        attr: A string that represents the name of the attribute.
        
        typ: An optional parameter that specifies the type of the attribute. If this parameter is not provided, the validate parameter must be a callable that takes an object and returns a boolean value indicating whether the object is valid.
        
        validate: An optional parameter that specifies a callable that takes an object and returns a boolean value indicating whether the object is valid. If this parameter is not provided, the typ parameter must be a type object.
        
        default: An optional parameter that specifies the default value of the attribute.
        
        getter -> get: An optional parameter that specifies a callable that returns the value of the attribute. This is useful if the attribute is computed or if it needs to be retrieved from a different location.
        In summary, the Attribute class is used to define an attribute with a name, a type or validation function, a default value, and an optional getter function. The typ and validate parameters are mutually exclusive, and at least one of them must be provided. If typ is provided, the validate function is automatically generated to check if the value is an instance of typ. If validate is provided, it is used to validate the value instead.
    """

    def __init__(
        self,
        attr: str,
        typ: type | None = None,
        validate: Callable[[object], bool] | None = None,
        default: bool = False,
        getter: Callable[[object], object] = None,
    ):
        self.attr = attr
        if typ is None and validate is Callable[[object], bool]:
            self.validate = validate
        elif validate is None and typ is not None:
            self.typ = typ
            self.validate = (
                lambda a: isinstance(a, typ) if not hasattr(self, "get") else self.get
            )
            if getter is not None:
                self.get = getter
        else:
            raise SystemExit("No type!")
        self.default = default
    def get(object: object):
        return object

class InAttribute:

    def __init__(self, attr: str, options: List[Attribute], validateAll: bool = True):
        self.attr = attr
        self.validateAll = validateAll
        option = Option("sub_"+attr, attr)
        for x in options:
            option.append(x)
        self.options = AppSettings([option])
class Option:
    """_summary_
    In the Option class, optionID is a unique identifier for the option, while optionName is the name of the option. The optionID is used to differentiate between different options, while the optionName is used to identify the option in the settings data.
    """

    def __init__(
        self, name: str, optionName: str = "name"
    ):
        self.name = name
        self.optionName = optionName
        self.attributes = []
        self.default = None

    def append(self, attribute: Attribute | InAttribute):
        if self.default is None:
            self.default = attribute
        if type(attribute) is Attribute and attribute.default:
            self.default = attribute
        self.attributes.append(attribute)

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
            actual_name = option.name
            actual_optionName = option.optionName
            if type(option.default) is Attribute:
                all.append(specialDict(actual_optionName, self.getSetting(actual_name, actual_optionName).default.default))
            else:
                #getSetting must import InAttribute recursive                       ###################################################################
                for sub_preload in option.default.options:
                    if type(sub_preload) is Attribute:
                        continue
                    sub_preloaded = sub_preload.preload()
                    all.append(specialDict(actual_optionName,sub_preloaded))
        return all
    def validateAll(self):
        i = 0
        for key, value in self.dict.items():
            for option in self.options:
                if (
                    option.optionName in value
                ):
                    for attr in [
                        y for y in list(value.keys()) if y != option.optionName
                    ]:
                        attr_get = getWithAttr(option.attributes, attr, "attr")
                        val = attr_get.validate(value[attr])
                        if attr in [x.attr for x in option.attributes] and not val:
                            raise SystemExit(
                                f"Value ({value[attr]}) [{i}] Validation Failure for {attr_get.attr} of {option.name}"
                            )
                        if callable(val):
                            value[attr] = val()
                    self.dict[option.name] = value
                    self.defaults[option.name] = value[option.default.attr]
            i += 1

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
                    self.dict[option.name] = statement
                    self.defaults[option.name] = statement[option.default.attr]

    def getSetting(self, name: str, attr: str | None):
        def getSettingClosure():
            value = getWithAttr(self.options, name, "name")
            if value is not None:
                return value
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
            result = {}
            for sub_attr in attr_get.options:
                sub_attr_get = getWithAttr(option.attributes, sub_attr.attr, "attr")
                if sub_attr_get is None:
                    raise KeyError(f"Attribute {sub_attr.attr} not found in {option.name}")
                result[sub_attr.attr] = getSettingClosure()
            return result
        else:
            # try:
                return getSettingClosure()
            # except KeyError:
            #     return self.defaults[name].default
        # except KeyError:
        #     raise KeyError(f"Attribute {attr} not found in settings")

    def getSettings(self):
        return self.dict
    
    def writeSetting(self, name: str, attr: str, value: Any):
        self.dict[name]= specialDict(attr, value)
        
    def getDefaultSettings(self):
        return self.defaults

    def __str__(self):
        text = ""
        for property, value in vars(self).items():
            text += " ".join([str(x) for x in [property, ":", value]])
            text += "\n"
        return text
