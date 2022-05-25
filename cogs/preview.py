import io

from discord.ext import commands
from discord.commands import slash_command
from discord import Option
from discord import File

from discord import context

from fonts import fonts
from defines import text
from preferences import get_preference
from colour import rgb_tuple
import sitelen

class CogPreview(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name="preview")
        async def command_preview(ctx, *, text):
            if text.startswith("text:"):
                text = text.replace("text:", "", 1)
            await preview(ctx, text)

    @slash_command(
      name='preview',
      description=text["DESC_PREVIEW"],
    )
    async def slash_preview(self, ctx, text: Option(str, text["DESC_PREVIEW_OPTION"])):
        await preview(ctx, text)


async def preview(ctx, text):
    fontsize = get_preference(str(ctx.author.id), "fontsize")
    color = get_preference(str(ctx.author.id), "color")
    images = []
    for font in fonts:
        images.append(sitelen.display(text, fonts[font], fontsize, rgb_tuple(color)))
    if isinstance(ctx, context.ApplicationContext):
        await ctx.respond(file=File(io.BytesIO(sitelen.stitch(images)), filename="a.png"))
    else:
        await ctx.send(file=File(io.BytesIO(sitelen.stitch(images)), filename="a.png"))

