import os

from discord.ext import commands
from dotenv import load_dotenv

# from discord import Intents


TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

from ilo.cogs.acro import CogAcro
from ilo.cogs.borgle import CogBorgle
from ilo.cogs.lp import CogLp
from ilo.cogs.nimi import CogNimi
from ilo.cogs.preferences import CogPreferences
from ilo.cogs.preview import CogPreview
from ilo.cogs.prompt import CogPrompt
from ilo.cogs.se import CogSe
from ilo.cogs.sp import CogSp
from ilo.cogs.ss import CogSs
from ilo.cogs.stest import CogStest

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


if __name__ == "__main__":
    bot.add_cog(CogAcro(bot))
    bot.add_cog(CogNimi(bot))
    bot.add_cog(CogPreferences(bot))
    bot.add_cog(CogLp(bot))
    bot.add_cog(CogSp(bot))
    bot.add_cog(CogSs(bot))
    bot.add_cog(CogSe(bot))
    bot.add_cog(CogPreview(bot))
    bot.add_cog(CogBorgle(bot))
    bot.add_cog(CogStest(bot))
    bot.add_cog(CogPrompt(bot))
    bot.run(TOKEN, reconnect=True)
