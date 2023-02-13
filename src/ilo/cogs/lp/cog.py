from discord.ext.commands import Cog
from discord.commands import slash_command, option

from ilo.defines import text
from ilo import jasima


class CogLp(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="lp", description=text["DESC_LP"])
    @option(name="word", description=text["DESC_LP_OPTION"])
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
