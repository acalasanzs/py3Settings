import questionary

color = questionary.select(
    "Select a color:",
    choices=[
        "Red",
        "Blue",
        "Yellow",
        "Green",
        "Orange",
        "Purple",
        "Pink",
        "Brown",
        "Gray",
    ],
).ask()

print(f"You selected the color {color}.")