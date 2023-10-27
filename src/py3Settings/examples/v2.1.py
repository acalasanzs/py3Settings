import click
from colorama import Fore, Style
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
@click.command()
@click.option('--option', prompt='Enter option name', help='Name of the option')
@click.option('--attribute', prompt='Enter attribute name', help='Name of the attribute')
def get_setting(option, attribute):
    attr_value = app_settings.getSetting(option, attribute)
    click.echo(Fore.GREEN + f"{attribute} value for {option}: {attr_value}" + Style.RESET_ALL)

# Get all settings data
@click.command()
def get_settings():
    settings_data = app_settings.getSettings()
    click.echo(Fore.GREEN + "All settings data:" + Style.RESET_ALL)
    click.echo(settings_data)

# Get default settings data
@click.command()
def get_default_settings():
    default_settings_data = app_settings.getDefaultSettings()
    click.echo(Fore.GREEN + "Default settings data:" + Style.RESET_ALL)
    click.echo(default_settings_data)

# Save settings data to a file
@click.command()
@click.option('--file', prompt='Enter file path', help='Path to the file to save settings data')
def save_settings(file):
    app_settings.saveFile(file)
    click.echo(Fore.GREEN + "Settings data saved to file successfully!" + Style.RESET_ALL)

# Create a group of commands
@click.group()
def cli():
    pass

# Add commands to the group
cli.add_command(get_setting)
cli.add_command(get_settings)
cli.add_command(get_default_settings)
cli.add_command(save_settings)

if __name__ == '__main__':
    cli()
