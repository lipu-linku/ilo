import io

from discord.ext import commands
from discord.commands import slash_command
from discord import Option
from discord import File

from discord import context

from defines import fonts
from defines import text
from preferences import get_preference
import sitelenpona

class CogSp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name="sp")
        async def command_sp(ctx, *, text):
            if text.startswith("text:"):
                text = text.replace("text:", "", 1)
            await sp(ctx, text)

    @slash_command(
      name='sp',
      description=text["DESC_SP"],
    )
    async def slash_sp(self, ctx, text: Option(str, text["DESC_SP_OPTION"])):
        await sp(ctx, text)

async def sp(ctx, text):
    fontsize = get_preference(str(ctx.author.id), "fontsize")
    font = get_preference(str(ctx.author.id), "font")
    if isinstance(ctx, context.ApplicationContext):
        await ctx.respond(file=File(io.BytesIO(sitelenpona.display(text, fonts[font], fontsize)), filename="a.png"))
    else:
        await ctx.send(file=File(io.BytesIO(sitelenpona.display(text, fonts[font], fontsize)), filename="a.png"))
