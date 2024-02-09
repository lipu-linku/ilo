import json
import os
import random
import urllib.request
from typing import Dict, List, Optional, Tuple

from sona.fingerspelling import Fingerspelling
from sona.fingerspelling_sign import FingerspellingSign
from sona.font import Font
from sona.fonts import Fonts
from sona.languages import Languages
from sona.sign import Sign
from sona.signs import Signs
from sona.word import Word
from sona.words import Words

WORDS_LINK = "https://api.linku.la/v1/words?lang=*"
LANGUAGES_LINK = "https://api.linku.la/v1/languages"
FONTS_LINK = "https://api.linku.la/v1/fonts"
SIGNS_LINK = "https://api.linku.la/v1/luka_pona/signs"
FINGERSPELLING_LINK = "https://api.linku.la/v1/luka_pona/fingerspelling"

help_message = "The word you requested, ***{}***, is not in the database I use. Make sure you didn't misspell it, or talk to kala Asi if this word really is missing."
multiple_words_message = "The phrase you requested, ***{}***, contains multiple words. I am but a simple dictionary and can only do words one at a time."
exception_nonspecific = "Something failed and I'm not sure what. Please tell kala Asi."

USAGE_MAP = {  # TODO: do not hardcode? serve from api?
    "core": 90,
    "widespread": 70,
    "common": 50,
    "uncommon": 20,
    "rare": 10,
    "obscure": 0,
}

USAGES = list(USAGE_MAP.keys())
SITELEN_SITELEN_FONT = "sitelen Latin (ss)"
DEFAULT_FONT = "nasin sitelen pu mono"

# TODO:
# - rework all functions here to use the api
# - find all `jasima` and replace it with `data`
# - find all `bundle` and replace it with a function from `data`


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


# Fonts need to be inverted to `name` for user purposes;
# from there, the user only needs the filename, since it's for preferences
FONTDIR = "ijo/nasinsitelen/"
USABLE_FONTS = {
    font: os.path.join(FONTDIR, fontdata["filename"])
    for font, fontdata in FONTS_DATA.items()
    if "filename" in fontdata
}
USABLE_FONTS = {k: v for k, v in USABLE_FONTS.items() if os.path.exists(v)}

# Luka pona data needs to be inverted to `definition` for the LpCog
LUKAPONA_DATA_BY_WORD: Dict[str, Sign] = {
    v["definition"]: v for _, v in SIGNS_DATA.items()
}

LANGUAGES = list(LANGUAGE_DATA.keys())
FONTS = list(FONTS_DATA.keys())
FONTS_FOR_AUTOCOMPLETE = list(USABLE_FONTS)
WORDS = list(WORDS_DATA.keys())


def get_word_data(word: str) -> Optional[Word]:
    """Fetch a word from sona or return None."""
    return WORDS_DATA.get(word)


def get_lukapona_data(word: str) -> Sign:
    return LUKAPONA_DATA_BY_WORD[word]


def get_random_word(min_usage: str = "widespread") -> Tuple[str, Word]:
    word = random.choice(get_words_min_usage_filter(min_usage))
    response = get_word_data(word)
    return word, response


def get_languages_for_slash_commands():
    # TODO: make constant
    lang_opts = dict()
    for k, v in LANGUAGE_DATA.items():
        names = v["name"]
        name = names.get("endonym") or names["en"]
        lang_opts[name] = k
    return


def get_usages_for_slash_commands() -> dict:  # it expects a dict for pref choices
    return {usage: usage for usage in USAGE_MAP}


def get_usage(word: str) -> int:
    """Given a word, return the usage of that word if it exists or 0"""
    if word_data := WORDS_DATA.get(word):
        if usages := word_data.get("usage"):  # in case a word has no usage
            if last_usage := list(usages.values())[-1]:  # always last member
                return last_usage
    return 0


def get_words_min_usage_filter(usage: str):
    """Make autocomplete better for word selection, prune to only words at or above selected usage"""
    return [word for word in WORDS if get_usage(word) >= USAGE_MAP[usage]]


def fetch_font_filename(fontname: str) -> str:
    pass
