import logging
import os
import uuid

from discord import ApplicationContext
from discord.ext import bridge, commands
from dotenv import load_dotenv

from ilo.log_config import configure_logger

LOG = logging.getLogger("ilo")

# from discord import Intents


TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise EnvironmentError("No discord token found in the environment!")

LOG_LEVEL = os.getenv("LOG_LEVEL")
if not LOG_LEVEL:
    LOG_LEVEL = "INFO"

LOG_LEVEL_INT = getattr(logging, LOG_LEVEL.upper())

DEBUG_GUILDS = os.getenv("DEBUG_GUILDS")
if DEBUG_GUILDS:
    DEBUG_GUILDS = [
        int(n) for n in os.environ["DEBUG_GUILDS"].split(",") if n and n.isdigit()
    ]


bot = bridge.Bot(
    command_prefix=commands.when_mentioned_or("/"),
    debug_guilds=DEBUG_GUILDS,
    # intents=Intents.all(),
)


@bot.event
async def on_ready():
    for index, guild in enumerate(bot.guilds):
        print("{}) {}".format(index + 1, guild.name))


@bot.event
async def on_application_command_error(ctx: ApplicationContext, error: BaseException):
    await ctx.respond(f"Something went wrong!\n{error}", ephemeral=True)
    raise error  # ensure we get full stacktrace


@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.author == bot.user:
        if reaction.emoji == "❌":
            await reaction.message.delete()


def load_extensions():
    cogs_path = os.path.dirname(__file__) + "/cogs/"
    for cogname in sorted(os.listdir(cogs_path), key=len):
        path = cogs_path + cogname
        if os.path.isdir(path):
            if "__init__.py" in os.listdir(path):
                LOG.info("Loading cog %s", cogname)
                bot.load_extension(f"ilo.cogs.{cogname}")


if __name__ == "__main__":
    configure_logger("ilo", log_level=LOG_LEVEL_INT)
    configure_logger("discord", log_level=logging.WARNING)
    load_extensions()
    bot.run(TOKEN, reconnect=True)
