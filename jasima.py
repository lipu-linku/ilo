#!/bin/python3

import urllib.request
import json

from defines import extraemoji

JSON_LINK = "https://lipu-linku.github.io/jasima/data.json"
LANGUAGE_OPTIONS_PATH = "slashcommands/language_options.json"

help_message = "The word you requested, ***{}***, is not in the database I use. Make sure you didn't misspell it, or talk to kala Asi if this word really is missing."
multiple_words_message = "The phrase you requested, ***{}***, contains multiple words. I am but a simple dictionary and can only do words one at a time."
sheets_fail = "Something's wrong, I think I failed to reach Google Sheets. Please tell kala Asi."
exception_nonspecific = "Something failed and I'm not sure what. Please tell kala Asi."


def get_site(link):
    return urllib.request.urlopen(link).read().decode('utf8')


def get_word_entry(word):
    entries = bundle["data"]
    if len(word.split()) > 1:
        return multiple_words_message.format(word)
    if word not in entries:
        return help_message.format(word)
    return entries[word]


def sitelen_emosi(word):
        entries = bundle["data"]
        if word in entries:
            if "sitelen_emosi" in entries[word]:
                return entries[word]["sitelen_emosi"]
        chars = []
        for letter in word:
            chars.append(extraemoji[letter])
        return " ".join(chars)


def get_languages_for_slash_commands():
    languages = bundle["languages"]
    return {v["name_endonym"]: k for k, v in languages.items()}


bundle = json.loads(get_site(JSON_LINK))
