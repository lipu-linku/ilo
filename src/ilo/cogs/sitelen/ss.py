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


class CogSs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="ss",
        description=text["DESC_SS"],
    )
    async def slash_ss(self, ctx, text: Option(str, text["DESC_SS_OPTION"])):
        await ss(ctx, text)


async def ss(ctx, text):
    fontsize = preferences.get(str(ctx.author.id), "fontsize")
    color = preferences.get(str(ctx.author.id), "color")
    font = "sitelen Latin (ss)"
    image = io.BytesIO(sitelen.display(text, fonts[font], fontsize, rgb_tuple(color)))
    await ctx.respond(file=File(image, filename="a.png"))
