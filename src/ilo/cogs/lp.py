from discord.ext import commands
from discord.commands import slash_command
from discord import Option

from discord import context

from ilo.defines import text
from ilo import jasima

class CogLp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name="lp")
        async def command_lp(ctx, word):
            if word.startswith("word:"):
                word = word.replace("word:", "", 1)
            await lp(ctx, word)

    @slash_command(
      name='lp',
      description=text["DESC_LP"],
    )
    async def slash_lp(self, ctx, word: Option(str, text["DESC_LP_OPTION"])):
        await lp(ctx, word)

async def lp(ctx, word):
    response = jasima.get_word_entry(word)
    if isinstance(response, str):
        await ctx.send(response)
        return
    if "luka_pona" in response:
        if "gif" in response["luka_pona"]:
            if isinstance(ctx, context.ApplicationContext):
                await ctx.respond(response["luka_pona"]["gif"])
            else:
                await ctx.send(response["luka_pona"]["gif"])
            return
    if isinstance(ctx, context.ApplicationContext):
        await ctx.respond(f"No luka pona available for **{word}**")
    else:
        await ctx.send(f"No luka pona available for **{word}**")
