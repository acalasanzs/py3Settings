from init import *
# Define an attribute for the option
"""TODO
    *1. Add support for multiple conditions asides lambda, like int determiantors, etc.
"""
attr1 = Attribute("attr1", lambda x: x > 0, default=1)

# Define another attribute for the option
attr2 = Attribute("attr2", lambda x: len(x) > 0, default="default_value")

# Create an option with the attributes
my_option = Option("my_option", optionID="option_id")
my_option.append(attr1)
my_option.append(attr2)

# Create a list of options
options = [my_option]

# Create an instance of the AppSettings class with the options
app_settings = AppSettings(options)

# Validate the settings data
app_settings.validateAll()

# Get the value of an attribute for an option
attr1_value = app_settings.getSetting("my_option", "attr1")
print(attr1_value)

# Get all settings data
settings_data = app_settings.getSettings()

# Get default settings data
default_settings_data = app_settings.getDefaultSettings()

# Save settings data to a file
app_settings.saveFile(r"C:\Users\acses\Documents\py3Settings\tests\settings.json")