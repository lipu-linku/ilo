import os

from discord.ext import commands
from dotenv import load_dotenv

# from discord import Intents


TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")


bot = commands.Bot(
    command_prefix="/",
    # intents=Intents.all(),
)


@bot.event
async def on_ready():
    for index, guild in enumerate(bot.guilds):
        print("{}) {}".format(index + 1, guild.name))


@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.author == bot.user:
        if reaction.emoji == "❌":
            await reaction.message.delete()


def load_extensions():
    for cogname in os.listdir("./src/ilo/cogs/"):
        path = "./src/ilo/cogs/" + cogname
        if os.path.isdir(path):
            if "__init__.py" in os.listdir(path):
                bot.load_extension(f"ilo.cogs.{cogname}")

if __name__ == "__main__":
    load_extensions()
    bot.run(TOKEN, reconnect=True)
