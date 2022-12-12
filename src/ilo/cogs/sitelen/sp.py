import io

from discord.ext import commands
from discord.commands import slash_command
from discord import Option
from discord import File

from ilo.fonts import fonts
from ilo.defines import text
from ilo.preferences import preferences
from ilo.colour import rgb_tuple
from ilo import sitelen


def setup(bot):
    bot.add_cog(CogSp(bot))


class CogSp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="sp",
        description=text["DESC_SP"],
    )
    async def slash_sp(self, ctx, text: Option(str, text["DESC_SP_OPTION"])):
        await sp(ctx, text)


async def sp(ctx, text):
    fontsize = preferences.get(str(ctx.author.id), "fontsize")
    font = preferences.get(str(ctx.author.id), "font")
    color = preferences.get(str(ctx.author.id), "color")
    image = io.BytesIO(sitelen.display(text, fonts[font], fontsize, rgb_tuple(color)))
    await ctx.respond(file=File(image, filename="a.png"))
