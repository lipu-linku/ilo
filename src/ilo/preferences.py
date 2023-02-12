import json
import os

from ilo.defines import text

PREFERENCES_PATH = "userdata/preferences.json"


class PreferenceHandler:
    def __init__(self):
        self.templates = {}
        if os.path.exists(PREFERENCES_PATH):
            self.userdata = self.from_json()
        else:
            self.userdata = {}
            self.to_json()

    def register(self, template):
        self.templates[template.name] = template

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


preferences = PreferenceHandler()
