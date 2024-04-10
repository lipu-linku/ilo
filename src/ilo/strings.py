import logging
from itertools import zip_longest
from typing import Any, Callable, Dict, Literal, cast

from ilo import data
from ilo.cog_utils import load_file
from ilo.data import get_sandbox_data, get_word_data
from sona.word import Word

LOG = logging.getLogger()

STRINGS = cast(dict[str, str], load_file(__file__, "locale.json"))

MAX_EMBED_SIZE = 900
# this is to fly under the requirement
CLIPPED_EMBED_SIZE = 750


### coalescing to human readable response
def __coalesce_resp(
    query: str,
    searchfunc: Callable[[str], Any],
    *args: list[Any],
    **kwargs: dict[Any, Any],
) -> tuple[Literal[True], Word] | tuple[Literal[False], str]:
    if len(query.split()) > 1:
        return False, STRINGS["multiple_words"].format(query)

    resp = searchfunc(query, *args, **kwargs)
    if not resp:
        return False, STRINGS["missing_word"].format(query)
    return True, resp


def handle_word_query(
    query: str,
    sandbox: bool = False,
) -> tuple[Literal[True], Word] | tuple[Literal[False], str]:
    if len(query.split()) > 1:
        return False, STRINGS["multiple_words"].format(query)

    resp = get_word_data(query)
    if resp:
        return True, resp

    sandbox_resp = get_sandbox_data(query)
    if sandbox and sandbox_resp:
        return True, sandbox_resp
    if (not sandbox) and sandbox_resp:
        return False, STRINGS["sandbox_word"].format(query)

    return False, STRINGS["missing_word"].format(query)


def handle_sign_query(
    query: str,
) -> tuple[Literal[True], Word] | tuple[Literal[False], str]:
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
        lang = etymt["language"]  # always defined
        word = etymu.get("word")
        alt = etymu.get("alt")
        defin = etymt.get("definition")

        etym_formatted = f"{lang}"

        if word:
            etym_formatted += f": {word}"
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
