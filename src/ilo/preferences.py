import json

from ilo.colour import is_colour
from ilo.defines import acro_choices, text
from ilo.fonts import fonts
from ilo.jasima import get_languages_for_slash_commands

PREFERENCES_PATH = "userdata/preferences.json"


class PreferenceHandler:
    def __init__(self):
        self.templates = [
            Template("fontsize", 72, validation=fontsize_validation),
            Template("color", "ffffff", validation=colour_validation),
            Template("acro", "ku suli", acro_choices),
            Template("font", "linja sike", {font: font for font in fonts}),
            Template("language", "en", get_languages_for_slash_commands()),
        ]
        self.templates = {template.name: template for template in self.templates}
        self.userdata = self.from_json()

    def from_json(self):
        with open(PREFERENCES_PATH, encoding="utf-8") as f:
            userdata = json.load(f)
        return userdata

    def to_json(self):
        with open(PREFERENCES_PATH, "w", encoding="utf-8") as f:
            json.dump(self.userdata, f, indent=2)

    def get(self, user_id, key):
        value = self.get_raw(user_id, key)
        if self.get_status(user_id, key, value) == "set":
            return value
        return self.get_default(key)

    def get_status(self, user_id, key, value):
        if not value:
            return "unset"
        if not self.templates[key].is_valid(value):
            return "invalid"
        return "set"

    def get_raw(self, user_id, key):
        if user_id in self.userdata:
            if key in self.userdata[user_id]:
                return self.userdata[user_id][key]
        return None

    def get_default(self, key):
        return self.templates[key].default

    def set(self, user_id, key, value):
        if user_id not in self.userdata:
            self.userdata[user_id] = {}
        self.userdata[user_id][key] = value
        self.to_json()

    def reset(self, user_id):
        if user_id in self.userdata:
            self.userdata.pop(user_id)
        self.to_json()


class Template:
    def __init__(self, name, default, choices=None, validation=lambda x: True):
        self.name = name
        self.default = default
        self.option_type = type(default)
        self.description = text["DESC_PREFS_{}".format(name.upper())]
        self.option_desc = text["DESC_PREFS_{}_OPTION".format(name.upper())]
        self.choices = choices
        self.validation = validation

    def is_valid(self, value):
        if not isinstance(value, self.option_type):
            return False
        if self.choices:
            if value not in self.choices.values():
                return False
        return True


def fontsize_validation(value):
    if not (value <= 500 and value >= 14):
        return "Font size is limited to the range from 14 to 500."
    return True


def colour_validation(value):
    if not is_colour(value):
        return "The string has to be a valid hexadecimal rgb colour, e.g. `2288ff`."
    return True


preferences = PreferenceHandler()
