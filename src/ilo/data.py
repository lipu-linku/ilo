import json
import os
import random
import urllib.request
from enum import Enum
from typing import Callable, Dict, Iterable, List, Optional, Tuple, TypeAlias

from sona.fingerspelling import Fingerspelling
from sona.fingerspelling_sign import FingerspellingSign
from sona.font import Font
from sona.fonts import Fonts
from sona.languages import Languages
from sona.sign import Sign
from sona.signs import Signs
from sona.word import Word
from sona.words import Words

JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None

API_URL = "https://api.linku.la/"

WORDS_LINK = "https://api.linku.la/v1/words?lang=*"
LANGUAGES_LINK = "https://api.linku.la/v1/languages"
FONTS_LINK = "https://api.linku.la/v1/fonts"
SIGNS_LINK = "https://api.linku.la/v1/luka_pona/signs?lang=*"
FINGERSPELLING_LINK = "https://api.linku.la/v1/luka_pona/fingerspelling?lang=*"


HEADERS = {  # pretend to be Chrome 120 for our api (thanks cloudflare)
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3"
}


def get_site(url: str) -> bytes:
    req = urllib.request.Request(url, headers=HEADERS)
    resp = urllib.request.urlopen(req).read().decode("utf-8")
    return resp


WORDS_DATA: Words = json.loads(get_site(WORDS_LINK))
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
    if "filename" in fontdata
    and os.path.exists(os.path.join(FONTDIR, fontdata["filename"]))
}
assert USABLE_FONTS, (
    "No usable fonts found! Is something wrong with the fontdir? %s" % FONTDIR
)


class Usage(Enum):
    core = 90
    widespread = 70
    common = 50
    uncommon = 20
    rare = 10
    obscure = 0


# map endonym or fallback english name to langcode
# user will see name but pref will save as langcode
LANGUAGES_FOR_PREFS = {
    langdata["name"].get("endonym", langdata["name"]["en"]): langcode
    for langcode, langdata in LANGUAGE_DATA.items()
}
USAGES_FOR_PREFS = {usage.name: usage.name for usage in Usage}

SITELEN_SITELEN_FONT = "sitelen Latin (ss)"
DEFAULT_FONT = "nasin sitelen pu mono"

# TODO:
# - rework all functions here to use the api
# - find all `jasima` and replace it with `data`


WORDS = list(WORDS_DATA.keys())


def get_word_data(word: str) -> Optional[Word]:
    return WORDS_DATA.get(word)


def get_lukapona_data(word: str) -> Optional[Sign]:
    return SIGNS_DATA_BY_WORD.get(word)


def get_random_word(min_usage: str = "widespread") -> Tuple[str, Word]:
    word = random.choice(get_words_min_usage_filter(min_usage))
    response = get_word_data(word)
    return word, response


def get_usage(word: str) -> int:
    """Given a word, return the usage of that word if it exists or 0"""
    return deep_get_callable(WORDS_DATA, word, "usage", dict.values, list, -1) or 0


def get_words_min_usage_filter(usage: str):
    """Make autocomplete better for word selection, prune to only words at or above selected usage"""
    return [word for word in WORDS if get_usage(word) >= Usage[usage].value]


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


def deep_get_callable(
    obj: JSON,
    *keys: int | str | Callable[[JSON], JSON],
) -> JSON:
    for key in keys:
        if isinstance(obj, Dict) and isinstance(key, str):
            obj = obj.get(key)
        elif isinstance(obj, List) and isinstance(key, int):
            obj = obj[key] if key < len(obj) else None
        elif isinstance(key, Callable):  # obj agnostic
            obj = key(obj)
        else:
            return None
    return obj


def deep_get_word_data(*keys: int | str) -> JSON:
    return deep_get(WORDS_DATA, *keys)  # type: ignore because `sona` is just more specific JSON


def deep_get_sign_data(*keys: int | str) -> JSON:
    return deep_get(SIGNS_DATA, *keys)


def deep_get_sign_data_by_word(*keys: int | str) -> JSON:
    return deep_get(SIGNS_DATA_BY_WORD, *keys)
