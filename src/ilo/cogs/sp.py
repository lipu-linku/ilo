import io

from discord.ext import commands
from discord.commands import slash_command
from discord import Option
from discord import File

from discord import context

from ilo.fonts import fonts
from ilo.defines import text
from ilo.preferences import preferences
from ilo.colour import rgb_tuple
from ilo import sitelen


class CogSp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name="sp")
        async def command_sp(ctx, *, text):
            if text.startswith("text:"):
                text = text.replace("text:", "", 1)
            await sp(ctx, text)

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
    if isinstance(ctx, context.ApplicationContext):
        await ctx.respond(
            file=File(
                io.BytesIO(
                    sitelen.display(text, fonts[font], fontsize, rgb_tuple(color))
                ),
                filename="a.png",
            )
        )
    else:
        await ctx.send(
            file=File(
                io.BytesIO(
                    sitelen.display(text, fonts[font], fontsize, rgb_tuple(color))
                ),
                filename="a.png",
            )
        )
