import json

def load(file_path):
    with open(f"defines/{file_path}.json", encoding="utf-8") as f:
        return json.load(f)

acro_choices = load("acro_choices")
colours = load("colours")
extraemoji = load("extraemoji")
text = load("text")
borgle_map = load("borgle_map")
pref_list = load("pref_list")
