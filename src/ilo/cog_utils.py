import json
from pathlib import Path
from typing import Dict, List

from discord import AutocompleteContext
from discord.commands import option as pycord_option
from discord.commands import slash_command as pycord_slash_command
from discord.ext.bridge import bridge_command as pycord_bridge_command
from discord.ext.commands import Cog as PycordCog

from ilo import data
from ilo.preferences import Template, preferences


def load_file(file_path, file_name) -> List[str] | Dict:
    path = Path(file_path).parent / file_name
    with open(path, encoding="utf-8") as f:
        if path.suffix == ".json":
            return json.load(f)
        return list(f.readlines())


def is_subsequence(s: str, opt: str) -> bool:
    s_idx, opt_idx = 0, 0
    s_len, opt_len = len(s), len(opt)
    s, opt = s.lower(), opt.lower()

    while s_idx < s_len and opt_idx < opt_len:
        if s[s_idx] == opt[opt_idx]:
            s_idx += 1
        opt_idx += 1

    return s_idx == s_len


def fuzzy_filter(s: str, opts: list[str]) -> List[str]:
    return [opt for opt in opts if is_subsequence(s, opt)]


def startswith_filter(s: str, opts: list[str]) -> List[str]:
    s = s.lower()
    return list(filter(lambda x: x.lower().startswith(s), opts))


def autocomplete_filter(s: str, opts: list[str]) -> List[str]:
    return fuzzy_filter(s, opts)


async def word_autocomplete(ctx: AutocompleteContext) -> List[str]:
    # we could pre-compute the usages to save some time
    usage: str = preferences.get(str(ctx.interaction.user.id), "usage")
    words = data.get_words_min_usage_filter(usage)
    return autocomplete_filter(ctx.value, words)


async def font_autocomplete(ctx: AutocompleteContext) -> List[str]:
    return autocomplete_filter(ctx.value, list(data.USABLE_FONTS.keys()))


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
