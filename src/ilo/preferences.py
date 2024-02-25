import json
import logging
import os
from typing import Any, Callable, Dict, Optional, Tuple

from ilo.data import deep_get

PREFERENCES_PATH = "userdata/preferences.json"


class PreferenceHandler:
    def __init__(self):
        self.templates: Dict[str, Template] = {}
        if os.path.exists(PREFERENCES_PATH):
            self.userdata = self.from_json()
        else:
            self.userdata = {}
            self.to_json()

    def register(self, template: "Template"):
        self.templates[template.name] = template

    def from_json(self):
        with open(PREFERENCES_PATH, encoding="utf-8") as f:
            userdata = json.load(f)
        return userdata

    def to_json(self):
        with open(PREFERENCES_PATH, "w", encoding="utf-8") as f:
            json.dump(self.userdata, f, indent=2)

    def validate(self, key, value) -> bool:
        template = self.templates[key]
        return template.is_valid(value)

    def get(self, user_id: str, key: str):
        return deep_get(self.userdata, user_id, key)

    def get_or_default(self, user_id: str, key: str):
        return self.get(user_id, key) or self.get_default(key)

    def get_status(self, user_id: str, key: str) -> Tuple[Any, str]:
        """Only used by preference lister"""
        value = self.get(user_id, key)
        default = self.get_default(key)

        if value is None:
            return default, "unset"
        if self.validate(key, value):
            return value, "set"
        return default, "invalid"

    def get_override(self, key: str, override: Any) -> Tuple[Any, Optional[str]]:
        """Not really *get*, just uses the same workflow and validation"""
        error_template = self.templates[key].invalid_resp
        default = self.get_default(key)

        if self.validate(key, override):
            return override, None
        return default, error_template.format(override, default)

    def get_or_resp(
        self,
        user_id: str,
        key: str,
        override: Any = None,
    ) -> Tuple[Any, Optional[str]]:
        default = self.get_default(key)
        if override:
            return self.get_override(key, override)

        value = self.get(user_id, key)
        if value is None:  # behave as valid assignment, but default
            return default, None

        error_template = self.templates[key].invalid_pref
        if not self.validate(key, value):  # assigned pref is bad
            self.set(user_id, key, default)  # replace it
            return default, error_template.format(value, default)
        return value, None

    def get_default(self, key: str):
        return self.templates[key].default

    def set(self, user_id: str, key: str, value: Any):
        if user_id not in self.userdata:
            self.userdata[user_id] = {}
        self.userdata[user_id][key] = value
        self.to_json()

    def reset(self, user_id):
        self.userdata.pop(user_id, None)
        self.to_json()


class Template:
    def __init__(
        self,
        locale: Dict[str, str],
        name: str,
        default: Any,
        choices: Optional[Dict] = None,
        validation: Callable[[Any], bool] = lambda _: True,
    ):
        self.locale = locale
        self.name = name
        self.default = default
        self.option_type = type(default)
        self.description = locale[f"prefs-{name}"]
        self.option_desc = locale[f"prefs-{name}-option"]
        self.choices = choices
        self.validation = validation
        # TODO: this started sucking fast
        self.invalid_resp = locale[f"prefs-{name}-fallback"]
        self.invalid_pref = locale[f"prefs-{name}-pref-invalid"]
        self.invalid_choice = locale[f"prefs-{name}-choice-invalid"]

    def is_valid(self, value):
        if not isinstance(value, self.option_type):
            return False
        if not self.validation(value):
            return False
        if self.choices:
            if value not in self.choices.values():
                return False
        return True


preferences = PreferenceHandler()
