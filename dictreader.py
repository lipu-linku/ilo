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

help_message = "The word you requested, ***{}***, is not in the database I use. Make sure you didn't misspell it, or talk to kala Asi if this word really is missing."
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


def build_dict_from_sheet(link):
    datasheet = get_site(link).split("\n")

    keys = datasheet.pop(0)[:-1].split("\t")
    entries = [line[:-1].split("\t") for line in datasheet]

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
        if word in entries:
            return entries[word]
        else:
            return help_message.format(word)


if __name__ == "__main__":
    build_json()
    #print(get_word_entry("alasa"))
    #upload_json_to_github()
