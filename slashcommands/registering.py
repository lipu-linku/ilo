import requests
import json

import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
APPLICATION = os.getenv('DISCORD_APPLICATION')

url = "https://discord.com/api/v8/applications/" + APPLICATION + "/commands"
headers = {"Authorization": "Bot " + TOKEN}

# Get commands
with open("commands.json") as f:
    json_commands = json.load(f)

# Remove currently registered commands
for command in requests.get(url, headers=headers).json():
    print("Deleted", command)
    requests.delete(url + "/" + command["id"], headers=headers)

# Register commands
for command in json_commands:
    print("Registered", command)
    requests.post(url, headers=headers, json=command)

# Print current commands
for command in requests.get(url, headers=headers).json():
    print(command)
