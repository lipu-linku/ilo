import json

def load(file_path):
    with open(f"defines/{file_path}.json") as f:
        return json.load(f)

acro_choices = load("acro_choices")
colours = load("colours")
defaults = load("defaults")
extraemoji = load("extraemoji")
fonts = load("fonts")
text = load("text")
