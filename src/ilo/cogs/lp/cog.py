from discord.ext import commands
from discord.commands import slash_command
from discord import Option

from ilo.defines import text
from ilo import jasima


def setup(bot):
    bot.add_cog(CogLp(bot))


class CogLp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="lp",
        description=text["DESC_LP"],
    )
    async def slash_lp(self, ctx, word: Option(str, text["DESC_LP_OPTION"])):
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
