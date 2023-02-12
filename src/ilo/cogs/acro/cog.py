from discord.ext import commands
from discord.commands import slash_command
from discord import Option

from ilo.defines import acro_choices
from ilo.defines import text
from ilo.preferences import preferences
from ilo.preferences import Template
from ilo import acronym


class CogAcro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        preferences.register(Template("acro", "ku suli", acro_choices))

    @slash_command(
        name="acro",
        description=text["DESC_ACRO"],
    )
    async def slash_acro(self, ctx, text: Option(str, text["DESC_ACRO_OPTION"])):
        await acro(ctx, text)


async def acro(ctx, text):
    book = preferences.get(str(ctx.author.id), "acro")
    await ctx.respond(acronym.respond(text, book))
