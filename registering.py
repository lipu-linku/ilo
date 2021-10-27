import requests

import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
APPLICATION = os.getenv('DISCORD_APPLICATION')

url = "https://discord.com/api/v8/applications/" + APPLICATION + "/commands"

json = {
    "name": "n",
    "type": 1,
    "description": "Get the translation of a toki pona word",
    "options": [
        {
            "name": "word",
            "description": "The word you want to get the translation of.",
            "type": 3,
            "required": True
        }
    ]
}

headers = {
    "Authorization": "Bot " + TOKEN
}

r = requests.post(url, headers=headers, json=json)

def delete_all_slash_commands():
    for command in requests.get(url, headers=headers).json():
        requests.remove(url + "/" + command.id, headers=headers)
