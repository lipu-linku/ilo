import io

from discord.ext import commands
from discord.commands import slash_command
from discord import Option
from discord import File

from discord import context

from fonts import fonts
from defines import text
from preferences import preferences
from colour import rgb_tuple
import sitelen

class CogSs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name="ss")
        async def command_ss(ctx, *, text):
            if text.startswith("text:"):
                text = text.replace("text:", "", 1)
            await ss(ctx, text)

    @slash_command(
      name='ss',
      description=text["DESC_SS"],
    )
    async def slash_ss(self, ctx, text: Option(str, text["DESC_SS_OPTION"])):
        await ss(ctx, text)

async def ss(ctx, text):
    fontsize = preferences.get(str(ctx.author.id), "fontsize")
    color = preferences.get(str(ctx.author.id), "color")
    font = "sitelen Latin (ss)"
    if isinstance(ctx, context.ApplicationContext):
        await ctx.respond(file=File(io.BytesIO(sitelen.display(text, fonts[font], fontsize, rgb_tuple(color))), filename="a.png"))
    else:
        await ctx.send(file=File(io.BytesIO(sitelen.display(text, fonts[font], fontsize, rgb_tuple(color))), filename="a.png"))
