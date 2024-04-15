# ilo Linku

<div align="center">
  <a href="https://discord.gg/A3ZPqnHHsy">
    <img src="https://img.shields.io/badge/-Discord-%237289da?style=for-the-badge&logo=appveyor">
  </a>
</div>

## Overview

**ilo Linku** is a Discord bot for toki pona, providing the Linku dictionary, font rendering, and other miscellaneous features.

## Self-hosting

### Prerequisites

To run in a Podman environment (default):

- Python 3.8+
- [pdm](https://github.com/pdm-project/pdm)
- [Podman](https://podman.io/)
- [Podman Compose](https://github.com/containers/podman-compose)

To run in Docker environment (see `Makefile`):

- Python 3.8+
- [pdm](https://github.com/pdm-project/pdm)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

To run locally:

- Python 3.8+
- [pdm](https://github.com/pdm-project/pdm)
- [fribidi](https://github.com/fribidi/fribidi)
- [libraqm](https://github.com/HOST-Oman/libraqm)
- Install your dependencies with pdm: `pdm install` or `make init`

You likely already have the last two, but a symptom of not having them is that `/sp` will emit normal text instead of sitelen pona!

### Setup

- Create a bot account on the [Discord developer portal](https://discord.com/developers/applications). Follow official Discord instructions for that.
- Make sure to enable the following in the developer portal:
  - Scopes:
    - bot
    - applications.commands
  - Permissions:
    - Send Messages
    - Send Messages in Threads
    - Embed Links
    - Attach Files
    - Use Slash Commands
- Save your bot token to a `.env` file as `DISCORD_TOKEN=longstringofcharactersyougotfromtheportal`.
- Run the bot: `make build up` or `make local`, if you want the containerized or local bot respectively.

## Contributing

<div align="center">
  <a href="https://github.com/lipu-linku/ilo/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=lipu-linku/ilo" />
  </a>
</div>

Feel free to post issues, fork the repo, and open pull requests with your changes.
You can also join the discord to contribute translations and talk to the maintainers.

## License

ilo Linku is licensed under the GNU General Public License Version 3.
