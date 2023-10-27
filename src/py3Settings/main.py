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
            my_option = Option("my_option", optionID="option_id")
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
    def to_dict(self):
        return {
            "attr": self.attr,
            "typ": self.typ.__name__ if self.typ is not None else None,
            "validate": self.validate.__name__ if self.validate is not None else None,
            "default": self.default,
        }

class InAttribute:

    def __init__(self, attr: str, options: List[Attribute], default: bool = False, validateAll: bool = True, getter: Callable[[], Any] = None):
        self.attr = attr
        if getter is not None:
            self.get = getter
        self.default = default
        self.options = options

    def default(self) -> dict:
        return {option.attr: option.default for option in self.options}
    def to_dict(self):
        return {
            "attr": self.attr,
            "options": [option.to_dict() for option in self.options],
            "default": self.default,
        }
class Option:
    """_summary_
    In the Option class, optionID is a unique identifier for the option, while optionName is the name of the option. The optionID is used to differentiate between different options, while the optionName is used to identify the option in the settings data.
    """

    def __init__(
        self, name: str, optionName: str = "name", optionID: str | None = None
    ):
        self.name = name
        self.optionName = optionName
        self.attributes = []
        self.default = None
        if optionID is None:
            raise SystemExit("No optionID!")
        self.optionID = optionID

    def append(self, attribute: Attribute | InAttribute):
        if self.default is None:
            self.default = attribute
        if attribute.default:
            self.default = attribute
        self.attributes.append(attribute)
    def to_dict(self):
        return {
            "name": self.name,
            "optionName": self.optionName,
            "optionID": self.optionID,
            "attributes": [attr.to_dict() for attr in self.attributes],
            "default": self.default.to_dict() if self.default is not None else None,
        }

formats = [handle(".json", file.JSON)]


def addFormatSupport(Handler: Handler):
    formats.append(Handler)


def showFileDefs():
    return file

class AppSettings(Mapping):
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
            random.append(Attribute("attr", type(data[key]), default=data[key]))
            options.append(random)
        return AppSettings(options)

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
                result = x.load(filename, path)
                for i, setting in enumerate(result):
                    result[i] = AppSettings.from_dict(setting)
                return result
        return False

    @staticmethod
    def _saveFile(data: list, filename: str, path=os.getcwd()):
        type = "." + filename.split(".")[1]
        for x in formats:
            if x.format == type:
                if len(filename) == 0:
                    filename = f"settings{x.format}"
                return x.save([option.to_dict() for option in data], filename=filename, path=path)
        return False

    def loadFile(self, *args, **kwargs):
        data = AppSettings._loadFile(*args, **kwargs)
        if data is False:
            raise SystemExit("Format not supported")
        return self.load(data)

    def saveFile(self, *args, **kwargs):
        return AppSettings._saveFile(self.options, *args, **kwargs)

    def preProcess(self, data: dict):
        return list(data.values())

    def validateAll(self):
        i = 0
        for key, value in self.dict.items():
            for option in self.options:
                if (
                    option.optionName in value
                    and value[option.optionName] == option.optionID
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
                    and statement[option.optionName] == option.optionID
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
        def getSettingClosure(value):
            if attr in self.options:
                return self.options[attr].get(value)
            else:
                return self.defaults[attr].get(value)

        if attr is None:
            return getSettingClosure(self.defaults[name])
        try:
            option = next((option for option in self.options if option.name == name), None)
            if option is None:
                raise KeyError(f"Option {name} not found in settings")

            attr_get = getWithAttr(option.attributes + option.inAttributes, attr, "attr")
            if attr_get is None:
                raise KeyError(f"Attribute {attr} not found in {option.name}")

            if isinstance(attr_get, InAttribute):
                result = {}
                for sub_attr in attr_get.options:
                    sub_attr_get = getWithAttr(option.attributes + option.inAttributes, sub_attr.attr, "attr")
                    if sub_attr_get is None:
                        raise KeyError(f"Attribute {sub_attr.attr} not found in {option.name}")
                    result[sub_attr.attr] = getSettingClosure(self.dict[name].get(sub_attr.attr, sub_attr.default))
                return result
            else:
                return getSettingClosure(self.dict[name][attr])
        except KeyError:
            raise KeyError(f"Attribute {attr} not found in settings")

    def getSettings(self):
        return self.dict
    
    def writeSetting(self, name: str, attr: str, value: Any):
        self.dict[name][attr] = value
        
    def getDefaultSettings(self):
        return self.defaults

    def __str__(self):
        text = ""
        for property, value in vars(self).items():
            text += " ".join([str(x) for x in [property, ":", value]])
            text += "\n"
        return text
