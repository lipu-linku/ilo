import json
import os
import random
import urllib.request
from enum import Enum
from typing import Dict, List, Optional, TypeAlias
import discord

from sona.fingerspelling import Fingerspelling
from sona.fonts import Fonts
from sona.languages import Languages
from sona.sign import Sign
from sona.signs import Signs
from ilo.word import Word

JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None

LANGUAGES_LINK = "https://api.linku.la/v1/languages"
FONTS_LINK = "https://api.linku.la/v2/fonts"
SIGNS_LINK = "https://api.linku.la/v1/luka_pona/signs?lang=*"
FINGERSPELLING_LINK = "https://api.linku.la/v1/luka_pona/fingerspelling?lang=*"


def generate_useragent():
    # lazily make a modern os+browser useragent to cachebust Cloudflare
    operating_systems = [
        "Windows NT 10.0; Win64; x64",
        "X11; Linux x86_64",
        "Linux; Android 10; K",
    ]
    os = random.choice(operating_systems)
    version = 122 + random.randint(-12, 0)

    return f"Mozilla/5.0 ({os}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36"


HEADERS = {  # pretend to be Chrome 120 for our api (thanks cloudflare)
    "User-Agent": generate_useragent(),
    "Cache-Control": "no-cache",
}


def get_site(url: str) -> bytes:
    req = urllib.request.Request(url, headers=HEADERS)
    resp = urllib.request.urlopen(req).read().decode("utf-8")
    return resp

FONTS_DATA: Fonts = json.loads(get_site(FONTS_LINK))
LANGUAGE_DATA: Languages = json.loads(get_site(LANGUAGES_LINK))
SIGNS_DATA: Signs = json.loads(get_site(SIGNS_LINK))
FINGERSPELLING_DATA: Fingerspelling = json.loads(get_site(FINGERSPELLING_LINK))

# sign data needs to be searched by `definition` for LpCog
# the default key is the ID, which is an adaptation of its gloss
SIGNS_DATA_BY_WORD: Dict[str, Sign] = {
    v["definition"]: v for _, v in SIGNS_DATA.items()
}


# font data needs to be filtered to usable fonts
FONTDIR = "ijo/nasinsitelen/"
USABLE_FONTS = {
    font: os.path.join(FONTDIR, fontdata["filename"])
    for font, fontdata in FONTS_DATA.items()
    if fontdata.get("filename")
    and os.path.exists(os.path.join(FONTDIR, fontdata["filename"]))
}
assert USABLE_FONTS, (
    "No usable fonts found! Is something wrong with the fontdir? %s" % FONTDIR
)


class UsageCategory(Enum):
    core = 90
    common = 60
    uncommon = 30
    obscure = 5
    sandbox = 0


# map endonym or fallback english name to langcode
# user will see name but pref will save as langcode
LANGUAGES_FOR_PREFS = {
    langdata["name"].get("endonym", langdata["name"]["en"]): langcode
    for langcode, langdata in LANGUAGE_DATA.items()
}
USAGES_FOR_PREFS = {usage.name: usage.name for usage in UsageCategory}

SITELEN_SITELEN_FONT = "sitelen sitelen open"
DEFAULT_FONT = "nasin sitelen pu mono"
DEFAULT_FONTSIZE = 72
DEFAULT_COLOR = "dcdcdc"
DEFAULT_BGSTYLE = "outline"
DEFAULT_LANGUAGE = "en"
DEFAULT_USAGE_CATEGORY = "common"
DEFAULT_PROXY = False

# TODO:
# - rework all functions here to use the api
# - find all `jasima` and replace it with `data`

# Don't reference these variables directly, instead use get_words() or get_word()
_WORDS: dict[Word] = {}
_FETCHED_LANGS: list[str] = []

async def fetch_lang_and_defer(lang: str, ctx: discord.Interaction, ephemeral = False):
    """Does the same thing as fetch_lang(), but defers an interaction if the translation has not already been downloaded. Use this in commands"""
    if lang not in _FETCHED_LANGS:
         await ctx.response.defer(ephemeral = ephemeral)
    return fetch_lang(lang)

def fetch_lang(lang: str) -> bool:
    """Downloads a language translation of the API if and only if it has not been downloaded already, otherwise does nothing."""
    if lang in _FETCHED_LANGS:
        return False
    _FETCHED_LANGS.append(lang)

    for key, value in (
        json.loads(get_site(f"https://api.linku.la/v2/words?lang={lang}")) |
        json.loads(get_site(f"https://api.linku.la/v2/sandbox?lang={lang}"))
    ).items():
        if not key in _WORDS:
            _WORDS[key] = Word(value)
        _WORDS[key].add_lang(lang, value)
    return True

def get_non_sandbox_word(word_str: str, lang: str = "en") -> Optional[Word]:
    return word if (word := get_word(word_str, lang)) and word.usage_category != "sandbox" else None

def get_sandbox_word(word_str: str, lang: str = "en") -> Optional[Word]:
    return word if (word := get_word(word_str, lang)) and word.usage_category == "sandbox" else None

def get_word(word_str: str, lang: str = "en") -> Optional[Word]:
    fetch_lang(lang)
    return _WORDS.get(word_str)

def get_non_sandbox_words(lang: str = "en") -> dict[Word]:
    fetch_lang(lang)
    return [word for word in _WORDS if word.usage_category != "sandbox"]

def get_sandbox_words(lang: str = "en") -> dict[Word]:
    fetch_lang(lang)
    return [word for word in _WORDS if word.usage_category == "sandbox"]

def get_words(lang: str = "en") -> dict[Word]:
    fetch_lang(lang)
    return _WORDS


def get_lukapona_data(word: str) -> Optional[Sign]:
    return SIGNS_DATA_BY_WORD.get(word)


def get_random_word(min_usage: str = "common") -> Word:
    word = random.choice(get_words_min_usage_filter(min_usage))
    return word


def get_words_min_usage_filter(usage: str):
    """Make autocomplete better for word selection, prune to only words at or above selected usage"""
    return [word for word in _WORDS.values() if word.get_usage() >= UsageCategory[usage].value]


def deep_get(obj: JSON, *keys: int | str) -> JSON:
    for key in keys:
        if isinstance(obj, Dict) and isinstance(key, str):
            obj = obj.get(key)
        elif isinstance(obj, List) and isinstance(key, int):
            obj = obj[key] if key < len(obj) else None
        else:
            # there is a key but no traversable obj
            # or a key that is incompatible with the current obj
            return None
    return obj


def deep_get_sign_data(*keys: int | str) -> JSON:
    return deep_get(SIGNS_DATA, *keys)


def deep_get_sign_data_by_word(*keys: int | str) -> JSON:
    return deep_get(SIGNS_DATA_BY_WORD, *keys)
