import json
import random
import urllib.request
from typing import List, Tuple

JSON_LINK = "https://lipu-linku.github.io/jasima/data.json"

help_message = "The word you requested, ***{}***, is not in the database I use. Make sure you didn't misspell it, or talk to kala Asi if this word really is missing."
multiple_words_message = "The phrase you requested, ***{}***, contains multiple words. I am but a simple dictionary and can only do words one at a time."
sheets_fail = (
    "Something's wrong, I think I failed to reach Google Sheets. Please tell kala Asi."
)
exception_nonspecific = "Something failed and I'm not sure what. Please tell kala Asi."

USAGE_MAP = {
    "core": 90,
    "widespread": 70,
    "common": 50,
    "uncommon": 20,
    "rare": 10,
    "obscure": 0,
}

USAGES = USAGE_MAP.keys()


def get_site(link):
    return urllib.request.urlopen(link).read().decode("utf8")


def get_word_entry(word):
    entries = bundle["data"]
    if len(word.split()) > 1:
        return multiple_words_message.format(word)
    if word not in entries:
        return help_message.format(word)
    return entries[word]


def latest_recognition_int(rec: dict) -> int:
    return int(list(rec.values())[-1]) or 0


def get_random_word(min_usage: str = "widespread") -> Tuple[str, dict]:
    entries = bundle["data"]
    word, response = random.choice(
        [
            (key, value)
            for key, value in entries.items()
            if latest_recognition_int(value["recognition"]) > USAGE_MAP[min_usage]
        ]
    )
    return word, response


def get_words_for_slash_commands():
    words = bundle["data"]
    return [word for word in words]


def get_languages_for_slash_commands():
    languages = bundle["languages"]
    return {v["name_endonym"]: k for k, v in languages.items()}


bundle = json.loads(get_site(JSON_LINK))
