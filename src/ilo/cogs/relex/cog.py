from discord.ext.commands import Cog
from discord.commands import slash_command, option

from ilo.defines import text
from ilo.relexer import relex


class CogRelex(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="relex", description=text["DESC_RELEX_EN"])
    @option(name="input", description=text["DESC_RELEX_INPUT"])
    async def slash_relex_en(self, ctx, input):
        await relex_command(ctx, input, "en")

    @slash_command(name="mama", description=text["DESC_RELEX_MAMA"])
    @option(name="input", description=text["DESC_RELEX_INPUT"])
    async def slash_relex_etym(self, ctx, input):
        await relex_command(ctx, input, "etym")


async def relex_command(ctx, input: str, method: str):
    relexed = relex(input, method)
    await ctx.respond(relexed)
