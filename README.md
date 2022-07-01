# ilo Linku
<div align="center">
<a  href="https://discord.gg/A3ZPqnHHsy"><img src="https://img.shields.io/badge/-Discord-%237289da?style=for-the-badge&logo=appveyor"></a>
</div>

## Overview
**ilo Linku** is a Discord bot for toki pona, providing the Linku dictionary, font rendering, and other miscellaneous features.

## Self-hosting

### Prerequisits
- Python 3.x

### Setup
- Create a bot account on the [Discord developer portal](https://discord.com/developers/applications). Follow official Discord instructions for that.
- Make sure to enable the following in the developer portal:
	- Intents:
		- Message Content Intent
	- Scopes:
		- bot
		- applications.commands
	- Permissions:
		- Send Messages
		- Send Messages in Threads
		- Embed Links
		- Attach Files
		- Use Slash Commands
- Install Python dependencies: `pip install -r requirements.txt`
- Save your bot token to a `.env` file as `DISCORD_TOKEN = longstringofcharactersyougotfromtheportal`.
- Run the bot: `python bot.py`

## License
ilo Linku is licensed under the GNU General Public License Version 3.
