from discord import ApplicationContext
from discord.ext.commands import Cog

from ilo import data
from ilo.cog_utils import Locale, word_autocomplete
from ilo.strings import handle_sign_query


class CogLp(Cog):
    def __init__(self, bot):
        self.bot = bot

    locale = Locale(__file__)

    @locale.command("lp")
    @locale.option("lp-word", autocomplete=word_autocomplete)
    @locale.option("lp-hide")
    async def slash_lp(self, ctx: ApplicationContext, word: str, hide: bool = True):
        await lp(ctx, word, hide)

    @locale.command("lukapona")
    @locale.option("lukapona-word", autocomplete=word_autocomplete)
    @locale.option("lukapona-hide")
    async def slash_lukapona(
        self, ctx: ApplicationContext, word: str, hide: bool = True
    ):
        await lp(ctx, word, hide)


async def lp(ctx: ApplicationContext, word: str, hide: bool = True):
    success, response = handle_sign_query(word)

    if not success:
        await ctx.respond(response, ephemeral=True)
        return
    if gif := data.deep_get(response, "video", "gif"):
        await ctx.respond(gif, ephemeral=hide)
        return
    await ctx.respond(f"No luka pona available for **{word}**", ephemeral=True)
