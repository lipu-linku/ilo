import urllib.request
import re
import json
import subprocess

import os
from dotenv import load_dotenv
load_dotenv()

DATA_LINK = os.getenv('GOOGLE_SHEETS_DATA_LINK')
LANGUAGES_LINK = os.getenv('GOOGLE_SHEETS_LANGUAGES_LINK')
GITHUB_ACCOUNT = "lipu-linku"
GITHUB_REPO = "jasima"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

JSON_PATH = "../jasima/data.json"
LANGUAGE_OPTIONS_PATH = "slashcommands/language_options.json"

help_message = "The word you requested, ***{}***, is not in the database I use. Make sure you didn't misspell it, or talk to kala Asi if this word really is missing."
multiple_words_message = "The phrase you requested, ***{}***, contains multiple words. I am but a simple dictionary and can only do words one at a time."
sheets_fail = "Something's wrong, I think I failed to reach Google Sheets. Please tell kala Asi."
exception_nonspecific = "Something failed and I'm not sure what. Please tell kala Asi."

def get_site(link):
    return urllib.request.urlopen(link).read().decode('utf8')


def build_json():
    languages = build_dict_from_sheet(LANGUAGES_LINK)
    data = build_dict_from_sheet(DATA_LINK)

    bundle = {"languages": languages, "data": data}
    with open(JSON_PATH, 'w') as f:
        json.dump(bundle, f, indent=2)
    return bundle


def build_dict_from_sheet(link):
    datasheet = get_site(link).split("\r\n")

    keys = datasheet.pop(0).split("\t")
    entries = [line.split("\t") for line in datasheet]

    ID_COLUMN = keys.index("id")
    keys.pop(ID_COLUMN)

    data = {}
    for line in entries:
        entry = {}
        entry_id = line.pop(ID_COLUMN)
        for index, value in enumerate(line):
            if value:
                if "/" not in keys[index]:
                    entry[keys[index]] = value
                else:
                    # e.g. 'def/en':
                    # outer = 'def'
                    # inner = 'en'
                    outer, inner = keys[index].split("/")
                    if outer not in entry:
                        entry[outer] = {}
                    entry[outer][inner] = value
        data[entry_id] = entry
    return data
    

def read_json():
    with open(JSON_PATH) as f:
        return json.load(f)


def upload_json_to_github():
    subprocess.call("git.bat {} {} {}".format(GITHUB_ACCOUNT, GITHUB_REPO, GITHUB_TOKEN))


def get_word_entry(word):
        bundle = read_json()
        entries = bundle["data"]
        if len(word.split()) > 1:
            return multiple_words_message.format(word)
        if word not in entries:
            return help_message.format(word)
        return entries[word]


def build_languages_for_slash_commands(languages):
    options = []
    for lang_id, language in languages.items():
        options.append({"name": language["name_endonym"], "value": lang_id})
    with open(LANGUAGE_OPTIONS_PATH, 'w') as f:
        json.dump(options, f, indent=4)
    

def routine():
    bundle = build_json()
    build_languages_for_slash_commands(bundle["languages"])
    upload_json_to_github()


if __name__ == "__main__":
    routine()
