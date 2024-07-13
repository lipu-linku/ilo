import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Literal

from discord import ApplicationContext, AutocompleteContext
from discord.ext.bridge import bridge_option
from discord.ext.bridge import bridge_command
from ilo import data
from ilo.preferences import preferences

LOG = logging.getLogger("ilo")

VALID_STYLES = ["outline", "background"]
BgStyle = Literal["outline"] | Literal["background"]

Color = tuple[int, int, int]
ColorAlpha = tuple[int, int, int, int]


async def handle_pref_error(
    ctx: ApplicationContext,
    user_id: str,
    key: str,
    override: Any = None,
):
    value, errmsg = preferences.get_or_resp(user_id, key, override=override)
    if errmsg is not None:
        await ctx.respond(errmsg, ephemeral=True)
    return value


def is_valid_language(value: str) -> bool:
    return value in data.LANGUAGE_DATA


def is_valid_usage_category(value: str) -> bool:
    return value in data.UsageCategory.__members__


def is_valid_font(value: str) -> bool:
    return value in data.USABLE_FONTS


def is_valid_fontsize(value: int) -> bool:
    return 14 <= value <= 500


def is_valid_color(value: str) -> bool:
    if re.match(r"^[0-9a-fA-F]{6}$", value):
        return True
    return False


def is_valid_bgstyle(style: BgStyle) -> bool:
    return style in VALID_STYLES


def load_file(file_path, file_name) -> List[str] | Dict:
    path = Path(file_path).parent / file_name
    with open(path, encoding="utf-8") as f:
        if path.suffix == ".json":
            return json.load(f)
        return list(f.readlines())


def rgb_tuple(value: str) -> Color | ColorAlpha:
    return tuple(bytes.fromhex(value))


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
    usage: str = preferences.get_or_default(str(ctx.interaction.user.id), "usage")
    words = data.get_words_min_usage_filter(usage)
    return autocomplete_filter(ctx.value, words)


async def font_autocomplete(ctx: AutocompleteContext) -> List[str]:
    return autocomplete_filter(ctx.value, list(data.USABLE_FONTS.keys()))


def build_autocomplete(options: list[str]):
    def autocompleter(ctx: AutocompleteContext):
        return autocomplete_filter(ctx.value, options)

    return autocompleter


class Locale:
    def __init__(self, file_path):
        self.locale = load_file(file_path, "locale.json")

    def __getitem__(self, key):
        return self.locale[key]

    def command(self, name, **kwargs):
        return bridge_command(name=name, description=self.locale[name], **kwargs)

    def option(self, name, **kwargs):
        return bridge_option(
            name=name.split("-")[-1], description=self.locale[name], **kwargs
        )
