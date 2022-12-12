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


class CogPreview(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="preview",
        description=text["DESC_PREVIEW"],
    )
    async def slash_preview(self, ctx, text: Option(str, text["DESC_PREVIEW_OPTION"])):
        await preview(ctx, text)


async def preview(ctx, text):
    fontsize = preferences.get(str(ctx.author.id), "fontsize")
    color = preferences.get(str(ctx.author.id), "color")
    images = []
    for font in fonts:
        images.append(sitelen.display(text, fonts[font], fontsize, rgb_tuple(color)))
    await ctx.respond(file=File(io.BytesIO(sitelen.stitch(images)), filename="a.png"))
