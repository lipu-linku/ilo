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
    async def slash_lp(self, ctx, word):
        await lp(ctx, word)

    @locale.command("lukapona")
    @locale.option("lukapona-word", autocomplete=word_autocomplete)
    async def slash_lukapona(self, ctx, word):
        await lp(ctx, word)


async def lp(ctx, word):
    response = handle_sign_query(word)

    if isinstance(response, str):
        await ctx.respond(response)
        return
    if gif := data.deep_get(response, "video", "gif"):
        await ctx.respond(gif)
        return
    await ctx.respond(f"No luka pona available for **{word}**")
