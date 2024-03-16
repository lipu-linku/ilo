from typing import Literal

from discord import ApplicationContext
from discord.ext.commands import Cog

from ilo.cog_utils import Locale
from ilo.relexer import relex
from ilo.strings import spoiler_text


class CogRelex(Cog):
    def __init__(self, bot):
        self.bot = bot

    locale = Locale(__file__)

    @locale.command("relex")
    @locale.option("relex-text")
    @locale.option("relex-spoiler")
    async def slash_relex_en(
        self, ctx: ApplicationContext, text: str, spoiler: bool = False
    ):
        await relex_command(ctx, text, spoiler, "en")

    @locale.command("mama")
    @locale.option("mama-text")
    @locale.option("mama-spoiler")
    async def slash_relex_etym(
        self, ctx: ApplicationContext, text: str, spoiler: bool = False
    ):
        await relex_command(ctx, text, spoiler, "etym")


async def relex_command(
    ctx, text: str, spoiler: bool = False, method: Literal["en", "etym"] = "en"
):
    relexed = relex(text, method)
    if spoiler:
        relexed = spoiler_text(relexed)
    await ctx.respond(relexed)
