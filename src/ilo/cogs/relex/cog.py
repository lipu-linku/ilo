from discord.ext.commands import Cog

from ilo.cog_utils import Locale, load_file
from ilo.relexer import relex


class CogRelex(Cog):
    def __init__(self, bot):
        self.bot = bot

    locale = Locale(__file__)

    @locale.command("relex")
    @locale.option("input")
    async def slash_relex_en(self, ctx, input):
        await relex_command(ctx, input, "en")

    @locale.command("mama")
    @locale.option("input")
    async def slash_relex_etym(self, ctx, input):
        await relex_command(ctx, input, "etym")


async def relex_command(ctx, input: str, method: str):
    relexed = relex(input, method)
    await ctx.respond(relexed)
