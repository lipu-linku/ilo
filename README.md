# ilo Linku: Toki Pona bot

This bot aims to support various Toki Pona needs on Discord, particularly [Sitelen Pona](https://sitelenpona.net/) and access to dictionaries such as [Linku](https://github.com/lipu-linku/sona/) and [Kemeka](https://github.com/pona-la/kemeka.pona.la/).

## Contributing

This is a collaborative project brought to you by the Toki Pona community.

<div align="center">
  <a href="https://github.com/lipu-linku/ilo/graphs/contributors">
    <img src="https://contrib.rocks/image?columns=9&max=27&repo=lipu-linku/ilo" />
  </a>
</div>

Your help is welcome! Feel free to submit pull requests if you find anything that needs improvement.

Want to help but you're [new to Github? We can help!](https://github.com/pona-la/.github/blob/main/help/README.md)

You can also join the Discord and talk to the maintainers!

<div align="center">
  <a href="https://discord.gg/A3ZPqnHHsy">
    <img src="https://raw.githubusercontent.com/pona-la/.github/refs/heads/main/assets/pali-pona-badge.svg">
  </a>
</div>

To run locally:

- `git submodule update --init`
- Install [uv](https://docs.astral.sh/uv/)
- Install [fribidi](https://github.com/fribidi/fribidi) and [libraqm](https://github.com/HOST-Oman/libraqm). On Linux you likely already have these. If not, `/sp` will fail!
- Follow the instructions in [Setup](#setup) to create a bot account.

Then:
- Run the bot: `uv run -m ilo`
- Run tests: `uv run pytest`

## Self-hosting

### Prerequisites

- `git submodule update --init`

To run in a Podman environment (default):

- [Podman](https://podman.io/)
- [Podman Compose](https://github.com/containers/podman-compose)

To run in Docker environment:

- [Docker](https://docs.docker.com/engine/)
- [Docker Compose](https://docs.docker.com/compose/)

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
- Run the bot: `podman compose up` or `docker compose up`.

## License

ilo Linku is licensed under [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).
