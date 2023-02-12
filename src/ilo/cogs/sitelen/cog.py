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


class CogSitelen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="sp",
        description=text["DESC_SP"],
    )
    async def slash_sp(self, ctx, text: Option(str, text["DESC_SP_OPTION"])):
        await sp(ctx, text)

    @slash_command(
        name="ss",
        description=text["DESC_SS"],
    )
    async def slash_ss(self, ctx, text: Option(str, text["DESC_SS_OPTION"])):
        await ss(ctx, text)

    @slash_command(
        name="preview",
        description=text["DESC_PREVIEW"],
    )
    async def slash_preview(self, ctx, text: Option(str, text["DESC_PREVIEW_OPTION"])):
        await preview(ctx, text)


async def sp(ctx, text):
    fontsize = preferences.get(str(ctx.author.id), "fontsize")
    font = preferences.get(str(ctx.author.id), "font")
    color = preferences.get(str(ctx.author.id), "color")
    image = io.BytesIO(sitelen.display(text, fonts[font], fontsize, rgb_tuple(color)))
    await ctx.respond(file=File(image, filename="a.png"))


async def ss(ctx, text):
    fontsize = preferences.get(str(ctx.author.id), "fontsize")
    color = preferences.get(str(ctx.author.id), "color")
    font = "sitelen Latin (ss)"
    image = io.BytesIO(sitelen.display(text, fonts[font], fontsize, rgb_tuple(color)))
    await ctx.respond(file=File(image, filename="a.png"))


async def preview(ctx, text):
    fontsize = preferences.get(str(ctx.author.id), "fontsize")
    color = preferences.get(str(ctx.author.id), "color")
    images = []
    for font in fonts:
        images.append(sitelen.display(text, fonts[font], fontsize, rgb_tuple(color)))
    await ctx.respond(file=File(io.BytesIO(sitelen.stitch(images)), filename="a.png"))
