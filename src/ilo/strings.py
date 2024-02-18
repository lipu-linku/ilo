import logging
from itertools import zip_longest
from typing import Any, Callable, Dict, cast

from ilo import data
from ilo.cog_utils import load_file
from ilo.data import get_word_data
from sona.sign import Sign
from sona.word import Word

LOG = logging.getLogger()

# Strings

STRINGS: Dict = cast(Dict, load_file(__file__, "locale.json"))

MAX_EMBED_SIZE = 1024
MAX_EMBED_SIZE = 900
# this is to fly under the requirement
CLIPPED_EMBED_SIZE = 750

### coalescing to human readable response


def __coalesce_resp(
    query: str,
    searchfunc: Callable[[str], Any],
    *args: Any,
    **kwargs: Any,
) -> str | Any:
    if len(query.split()) > 1:
        return STRINGS["multiple_words"]

    resp = searchfunc(query, *args, **kwargs)
    if not resp:
        return STRINGS["missing_word"]
    return resp


def handle_word_query(query: str) -> str | Word:
    return __coalesce_resp(query, get_word_data)


def handle_sign_query(query: str) -> str | Sign:
    return __coalesce_resp(query, data.get_lukapona_data)


### formatting


def clip_for_embed(to_embed: str):
    if len(to_embed) > MAX_EMBED_SIZE:
        to_embed = to_embed[:CLIPPED_EMBED_SIZE]
        to_embed += "…"
    return to_embed


def format_ku_data(ku_data: Dict[str, int]):
    """Take linku's ku data and format it like Sonja's ku data"""
    sorted_data = sorted(ku_data.items(), key=lambda x: x[1], reverse=True)
    to_format = []
    for word, score in sorted_data:
        to_format.append(f"{word}: {score}%")
    formatted = ", ".join(to_format)
    print(len(formatted))
    print(formatted)
    return clip_for_embed(formatted)


def format_etymology(
    etym_untrans: list[Dict[str, str]],
    etym_trans: list[Dict[str, str]],
):
    etyms_formatted = []
    for etymu, etymt in zip_longest(etym_untrans, etym_trans):
        lang = etymt["language"]
        word = etymu["word"]
        alt = etymu.get("alt")
        defin = etymt["definition"]

        etym_formatted = f"{lang}: {word}"
        if alt:
            etym_formatted += f" ({alt})"
        if defin:
            etym_formatted += f"; {defin}"
        etyms_formatted.append(etym_formatted)

    formatted = "\n".join(etyms_formatted)
    print(len(formatted))
    print(formatted)
    return clip_for_embed(formatted)


def spoiler_text(text: str):
    return f"||{text}||"
