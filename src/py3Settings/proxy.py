from typing import Callable
import re
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