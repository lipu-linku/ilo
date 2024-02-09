from typing import Dict, cast

from ilo.cog_utils import load_file
from ilo.data import WORDS, Word, get_word_data

# Strings

STRINGS: Dict = cast(Dict, load_file(__file__, "locale.json"))


def handle_word_query(query: str) -> str | Word:
    if len(query.split()) > 1:
        return STRINGS["multiple_words"]

    resp = get_word_data(query)
    if not resp:
        return STRINGS["missing_word"]

    return resp
