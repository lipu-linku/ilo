from discord import ApplicationContext
from discord.ext.commands import Cog

from ilo.cog_utils import Locale
from ilo.cogs.nimi.cog import Literal
from ilo.relexer import relex


class CogRelex(Cog):
    def __init__(self, bot):
        self.bot = bot

    locale = Locale(__file__)

    @locale.command("relex")
    @locale.option("relex-text")
    async def slash_relex_en(self, ctx: ApplicationContext, text: str):
        await relex_command(ctx, text, "en")

    @locale.command("mama")
    @locale.option("mama-text")
    async def slash_relex_etym(self, ctx: ApplicationContext, text: str):
        await relex_command(ctx, text, "etym")


async def relex_command(ctx, text: str, method: Literal["en", "etym"]):
    relexed = relex(text, method)
    await ctx.respond(relexed)
