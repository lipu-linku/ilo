from discord.commands import option, slash_command
from discord.ext.commands import Cog

from ilo import jasima
from ilo.cog_utils import Locale, load_file, word_autocomplete


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
    response = jasima.get_word_entry(word)
    if isinstance(response, str):
        await ctx.respond(response)
        return
    if "luka_pona" in response:
        if "gif" in response["luka_pona"]:
            await ctx.respond(response["luka_pona"]["gif"])
            return
    await ctx.respond(f"No luka pona available for **{word}**")
