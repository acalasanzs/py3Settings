import os
from typing import Any, Callable, Iterator, List
import file
from proxy import *
from utils import *
from collections.abc import Mapping

class AppSettings(Mapping):
    """
    A class for managing application settings.

    Parameters:
    options (List[Option]): A list of Option objects representing the available settings.

    Attributes:
    options (List[Option]): A list of Option objects representing the available settings.
    dict (dict): A dictionary containing the current settings.
    defaults (dict): A dictionary containing the default settings.
    i (int): An integer representing the current index when iterating over the settings.

    Methods:
    __getitem__(self, __key: str | int) -> Option: Returns the Option object with the given name or index.
    __delitem__(self, __key: str | int) -> None: Removes the Option object with the given name or index.
    __iter__(self): Returns an iterator over the Option objects.
    __len__(self) -> int: Returns the number of Option objects.
    __next__(self): Returns the next Option object when iterating over the settings.
    _loadFile(filename:str, path = os.getcwd()): Loads settings from a file.
    _saveFile(data: list, filename:str, path = os.getcwd()): Saves settings to a file.
    loadFile(self, *args,**kwargs): Loads settings from a file.
    saveFile(self, *args,**kwargs): Saves settings to a file.
    preProcess(data: dict): Preprocesses the settings data.
    validateAll(self): Validates all settings.
    load(self, data: list): Loads settings from a list.
    getSetting(self, name: str, attr: str | None): Returns the value of a setting.
    getSettings(self): Returns the current settings.
    getDefaultSettings(self): Returns the default settings.
    __str__(self): Returns a string representation of the AppSettings object.
    """
    def __init__(self, options: List[Option]):
        self.options = options
        self.dict = dict()
        self.defaults = dict()
        self.i = 0

    def __getitem__(self, __key: str | int) -> Option:
        """
        Returns the Option object with the given name or index.

        Parameters:
        __key (str | int): The name or index of the Option object to retrieve.

        Returns:
        Option: The Option object with the given name or index.
        """
        for i,x in enumerate(self.options):
            if __key == x.name or i == __key:
                return x

    def __delitem__(self, __key: str | int) -> None:
        """
        Removes the Option object with the given name or index.

        Parameters:
        __key (str | int): The name or index of the Option object to remove.
        """
        for i,x in enumerate(self.options):
            if __key == x.name or i == __key:
                self.options.remove(x)
                return

    def __iter__(self):
        """
        Returns an iterator over the Option objects.
        """
        return self

    def __len__(self) -> int:
        """
        Returns the number of Option objects.
        """
        return self.options.__len__()

    def __next__(self):
        """
        Returns the next Option object when iterating over the settings.
        """
        if self.__len__()  == self.i:
            raise StopIteration
        x = self.options[self.i]
        self.i += 1
        return x

    @staticmethod
    def _loadFile(filename:str, path = os.getcwd()):
        """
        Loads settings from a file.

        Parameters:
        filename (str): The name of the file to load.
        path (str): The path to the file.

        Returns:
        bool: True if the file was loaded successfully, False otherwise.
        """
        type = "."+filename.split(".")[1]
        for x in formats:
            if x.format == type:
                if(len(filename) == 0):
                    filename = f"settings{x.format}"
                return x.load(filename, path)
        return False

    @staticmethod
    def _saveFile(data: list, filename:str, path = os.getcwd()):
        """
        Saves settings to a file.

        Parameters:
        data (list): The settings data to save.
        filename (str): The name of the file to save to.
        path (str): The path to the file.

        Returns:
        bool: True if the file was saved successfully, False otherwise.
        """
        type = "."+filename.split(".")[1]
        for x in formats:
            if x.format == type:
                if(len(filename) == 0):
                    filename = f"settings{x.format}"
                return x.save(data, filename = filename, path = path)
        return False

    def loadFile(self, *args,**kwargs):
        """
        Loads settings from a file.

        Parameters:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

        Returns:
        bool: True if the file was loaded successfully, False otherwise.
        """
        data = AppSettings._loadFile(*args,**kwargs)
        if data is False:
            raise SystemExit("Format not supported")
        return self.load(data)

    def saveFile(self, *args,**kwargs):
        """
        Saves settings to a file.

        Parameters:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

        Returns:
        bool: True if the file was saved successfully, False otherwise.
        """
        return AppSettings._saveFile(AppSettings.preProcess(self.dict), *args,**kwargs)

    @staticmethod
    def preProcess(data: dict):
        """
        Preprocesses the settings data.

        Parameters:
        data (dict): The settings data to preprocess.

        Returns:
        list: The preprocessed settings data.
        """
        return list(data.values())

    def validateAll(self):
        """
        Validates all settings.
        """
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
        """
        Loads settings from a list.

        Parameters:
        data (list): The settings data to load.

        Raises:
        SystemExit: If a validation failure occurs.
        """
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
        """
        Returns the value of a setting.

        Parameters:
        name (str): The name of the setting.
        attr (str | None): The attribute of the setting.

        Returns:
        Any: The value of the setting.
        """
        if attr is None:
            return self.defaults[name]
        return self.dict[name][attr]

    def getSettings(self):
        """
        Returns the current settings.

        Returns:
        dict: The current settings.
        """
        return self.dict

    def getDefaultSettings(self):
        """
        Returns the default settings.

        Returns:
        dict: The default settings.
        """
        return self.defaults

    def __str__(self):
        """
        Returns a string representation of the AppSettings object.

        Returns:
        str: A string representation of the AppSettings object.
        """
        text = ""