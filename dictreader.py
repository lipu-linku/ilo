import urllib.request
import re
import json
import subprocess

import os
from dotenv import load_dotenv
load_dotenv()

DATA_LINK = os.getenv('GOOGLE_SHEETS_LINK')
GITHUB_ACCOUNT = "lipu-linku"
GITHUB_REPO = "jasima"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

JSON_PATH = "../jasima/data.json"

template = "***{}*** *~{}~* – {}\nSee more info on https://lipu-linku.github.io?q={}"
help_message = "The word you requested, ***{}***, is not in the database I use. Make sure you didn't misspell it, or talk to kala Asi if this word really is missing."
sheets_fail = "Something's wrong, I think I failed to reach Google Sheets. Please tell kala Asi."
exception_nonspecific = "Something failed and I'm not sure what. Please tell kala Asi."

def get_site(link):
    return urllib.request.urlopen(link).read().decode('utf8')


def build_json():
    entries = get_site(DATA_LINK).split("\n")
    keys = entries.pop(0)[:-1].split("\t")
    entries = [entry[:-1].split("\t") for entry in entries]
    entries_converted = []
    for entry in entries:
        entry_converted = {}
        entries_converted.append(entry_converted)
        for index, value in enumerate(entry):
            if value:
                entry_converted[keys[index]] = value
    with open(JSON_PATH, 'w') as f:
        # f.write("a = ") # to remove later!
        json.dump(entries_converted, f, separators=(',\n', ':'))


def read_json():
    with open(JSON_PATH) as f:
        return json.load(f)


def upload_json_to_github():
    subprocess.call("git.bat {} {} {}".format(GITHUB_ACCOUNT, GITHUB_REPO, GITHUB_TOKEN))


def get_word_entry(word):
    try:
        entries = read_json()
        response = []
        for entry in entries:
            if entry["word"] == word:
                response.append(template.format(entry["word"], entry["book"], entry["def_english"], entry["id"]))
        if response:
            return "\n".join(response)
        else:
            return help_message.format(word)
    except:
        return exception_nonspecific


if __name__ == "__main__":
    build_json()
    print(get_word_entry("alasa"))
    upload_json_to_github()
