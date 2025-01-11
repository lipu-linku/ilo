import logging
import os
import uuid

from discord import ApplicationContext, User
from discord.ext import bridge, commands
from discord.member import Member
from discord.permissions import Permissions
from discord.reaction import Reaction
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
async def on_reaction_add(reaction: Reaction, user: User | Member):
    message = reaction.message
    interaction = message.interaction_metadata
    if not message.author == bot.user:
        return  # not bot's message
    if not interaction:
        return  # not created by a command
    if not reaction.emoji == "❌":
        return  # not the delete react we chose

    # there is no way to obtain the single author of the triggering react
    async for user in reaction.users():
        if user == interaction.user:
            await reaction.message.delete()
            return

        # it can be null
        perms: Permissions | None = getattr(user, "guild_permissions", None)
        if perms and (perms.manage_messages or perms.administrator):
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
