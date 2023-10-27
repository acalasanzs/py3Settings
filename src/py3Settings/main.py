import os
from typing import Any, Callable, Iterator, List
import file
from proxy import *
from utils import *
from collections.abc import Mapping


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
    """

    def __init__(
        self,
        attr: str,
        typ: Any | None = None,
        validate: Callable[[object], bool] | None = None,
        default: bool = False,
        getter: Callable[[], Any] = None,
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

    def append(self, attribute: Attribute):
        if self.default is None:
            self.default = attribute
        if attribute.default:
            self.default = attribute
        self.attributes.append(attribute)


formats = [handle(".json", file.JSON)]


def addFormatSupport(Handler: Handler):
    formats.append(Handler)


def showFileDefs():
    return file


class AppSettings(Mapping):
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
        return AppSettings._saveFile(AppSettings.preProcess(self.dict), *args, **kwargs)

    @staticmethod
    def preProcess(data: dict):
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
        if attr is None:
            return self.defaults[name]
        try:
            return self.dict[name][attr]
        except:
            try:
                option = next((option for option in self.options if option.name == name), None)
                if option is None:
                    raise KeyError(f"Option {name} not found in settings")
                return option.default.default
            except KeyError:
                raise KeyError(f"Attribute {attr} not found in settings")

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
