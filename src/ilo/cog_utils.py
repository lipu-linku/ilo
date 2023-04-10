import json
from pathlib import Path
from typing import List

from discord import AutocompleteContext
from discord.commands import option as pycord_option
from discord.commands import slash_command as pycord_slash_command
from discord.ext.bridge import bridge_command as pycord_bridge_command
from discord.ext.commands import Cog as PycordCog

from ilo import jasima
from ilo.preferences import Template, preferences


def load_file(file_path, file_name):
    path = Path(file_path).parent / file_name
    with open(path, encoding="utf-8") as f:
        if path.suffix == ".json":
            return json.load(f)
        return list(f.readlines())


def startswith_filter(s: str, opts: list[str]):
    return list(filter(lambda x: x.lower().startswith(s.lower()), opts))


async def word_autocomplete(ctx: AutocompleteContext):
    usage: str = preferences.get(str(ctx.interaction.user.id), "usage")
    words = jasima.get_words_min_usage_filter(usage)
    return startswith_filter(ctx.value.lower(), words)


class Locale:
    def __init__(self, file_path):
        self.locale = load_file(file_path, "locale.json")

    def __getitem__(self, key):
        return self.locale[key]

    def command(self, name, **kwargs):
        return pycord_bridge_command(name=name, description=self.locale[name], **kwargs)

    def option(self, name, **kwargs):
        return pycord_option(
            name=name.split("-")[-1], description=self.locale[name], **kwargs
        )
