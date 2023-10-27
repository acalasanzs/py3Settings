import json
import sys
import os
sys.path.append(r'C:\Users\acses\Documents\py3Settings\src\py3Settings')
from main import AppSettings, Option, Attribute

# Define the structure of the settings
options = [
    Option("General", "general", [
        Attribute("name", str, default = "My App"),
        Attribute("version", str,default = "1.0.0"),
    ]),
    Option("Appearance", "appearance", [
        Attribute("theme", str,default = "Light"),
        Attribute("font_size", int,default = 12),
    ]),
]

# Create an instance of the AppSettings class
settings = AppSettings(options)
print(settings)
# Change the directory to the desired path
os.chdir(r'C:\Users\acses\Documents\py3Settings\tmpf')

# Your code here
settings.saveFile("default.json")
# settings.loadFile("settings.json")
