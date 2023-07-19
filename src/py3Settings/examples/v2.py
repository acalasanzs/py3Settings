"""
BEGIN
Path replacement
"""
import sys
import os.path
workdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
tests = os.path.abspath(os.path.join(workdir, *[os.path.pardir for _ in range(2)], 'tests'))
sys.path.append(workdir)
"""
END
Path replacement
"""
from main import AppSettings, Option, Attribute
from typing import List
options: List[Option] = list()
content = Option("content","warn","Already with content in it!")
content.append(Attribute("ask", bool))
exists = Option("exists","warn","{x} already exists!")
exists.append(Attribute("ask", bool))
settingsProxy = AppSettings([content,exists])
settingsProxy.loadFile("sure.json", tests)
print(settingsProxy)
settingsProxy.saveFile('algo.json', tests)
settingsProxy.validateAll()