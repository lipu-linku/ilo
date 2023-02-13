import json
from pathlib import Path

from discord.ext.commands import Cog as PycordCog
from discord.commands import slash_command as pycord_slash_command
from discord.commands import option as pycord_option


def load_file(file_path, file_name):
    path = Path(file_path).parent / file_name
    with open(path, encoding="utf-8") as f:
        if path.suffix == ".json":
            return json.load(f)
        return list(f.readlines())


class Locale:
    def __init__(self, file_path):
        self.locale = load_file(file_path, "locale.json")

    def command(self, name, **kwargs):
        return pycord_slash_command(name=name, description=self.locale[name], **kwargs)

    def option(self, name, **kwargs):
        return pycord_option(name=name.split("-")[-1], description=self.locale[name], **kwargs)
