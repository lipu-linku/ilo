from discord.commands import option, slash_command
from discord.ext.commands import Cog

from ilo.cog_utils import Locale, load_file, word_autocomplete
from ilo.data import get_lukapona_data
from ilo.strings import handle_word_query


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
    response = handle_word_query(word)
    # TODO: luka pona data is no longer with words

    if isinstance(response, str):
        await ctx.respond(response)
        return
    if gif := response.get("video", {}).get("gif"):
        await ctx.respond(gif)
        return
    await ctx.respond(f"No luka pona available for **{word}**")
