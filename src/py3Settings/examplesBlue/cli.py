import json
from main import AppSettings, Option, Attribute

# Define the structure of the settings
options = [
    Option("General", [
        Attribute("name", str, "My App"),
        Attribute("version", str, "1.0.0"),
    ]),
    Option("Appearance", [
        Attribute("theme", str, "Light"),
        Attribute("font_size", int, 12),
    ]),
]

# Create an instance of the AppSettings class
settings = AppSettings(options)

# Load settings from a JSON file (if it exists)
try:
    with open(os.path.join(os.path.dirname(__file__), "../../settings.json"), "r") as f:
        settings.load_json(f.read())
except FileNotFoundError:
    pass

# Prompt the user to update the settings
settings.update()

# Save the settings to a JSON file
with open(os.path.join(os.path.dirname(__file__), "../../settings.json"), "w") as f:
    f.write(json.dumps(settings.to_dict(), indent=4))