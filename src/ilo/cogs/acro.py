from discord.ext import commands
from discord.commands import slash_command
from discord import Option

from discord import context

from ilo.defines import text
from ilo.preferences import preferences
from ilo import acronym


class CogAcro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name="acro")
        async def command_acro(ctx, *, text):
            if text.startswith("text:"):
                text = text.replace("text:", "", 1)
            await acro(ctx, text)

    @slash_command(
        name="acro",
        description=text["DESC_ACRO"],
    )
    async def slash_acro(self, ctx, text: Option(str, text["DESC_ACRO_OPTION"])):
        await acro(ctx, text)


async def acro(ctx, text):
    book = preferences.get(str(ctx.author.id), "acro")
    if isinstance(ctx, context.ApplicationContext):
        await ctx.respond(acronym.respond(text, book))
    else:
        await ctx.send(acronym.respond(text, book))
