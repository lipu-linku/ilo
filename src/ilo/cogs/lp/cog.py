from discord.ext.commands import Cog
from discord.commands import slash_command, option

from ilo.cog_utils import Locale, load_file
from ilo import jasima


class CogLp(Cog):
    def __init__(self, bot):
        self.bot = bot

    locale = Locale(__file__)

    @locale.command("lp")
    @locale.option("lp-word")
    async def slash_lp(self, ctx, word):
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
