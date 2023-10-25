from typing import Callable
import re
def handle(format, dict:dict):
    ins = Handler(format)
    ins.init(**dict)
    return ins
class Handler:
    invalid = r'[<>:"/\|?* ]'
    def __init__(self, format: str):
        """
        Initializes a Handler object.

        Parameters:
        format (str): The format of the file to handle.
        """
        self.format = format

    def init(self, load: Callable[[str,str], dict], save: Callable[[dict], str | bool]):
        """
        Initializes the load and save functions.

        Parameters:
        load (Callable[[str,str], dict]): The function to load data from a file.
        save (Callable[[dict], str | bool]): The function to save data to a file.
        """
        self.load = Handler.safeCheck(load)
        self.save = Handler.safeCheck(save)

    @staticmethod
    def safeCheck(fun):
        """
        Wraps a function with a file string check.

        Parameters:
        fun (function): The function to wrap.

        Returns:
        function: The wrapped function.
        """
        def wrapper(*args, **kwargs):
            assert Handler.fileStr(kwargs.get('filename') or args[0])
            return fun(*args, **kwargs)
        return wrapper

    @classmethod
    def fileStr(cls, file: str) -> bool:
        """
        Checks if a file string is valid.

        Parameters:
        file (str): The file string to check.

        Returns:
        bool: True if the file string is valid, False otherwise.
        """
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