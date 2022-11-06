from discord.ext import commands
from discord.commands import slash_command
from discord import Option

from discord import context

from defines import sentences
from defines import text
import random

class CogStest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name="stest")
        async def command_stest(ctx):
            await stest(ctx)

    @slash_command(
      name='stest',
      description=text["DESC_STEST"],
    )
    async def slash_stest(self, ctx):
        await stest(ctx)


async def stest(ctx):
    index, sentence = random.choice(list(enumerate(sentences)))
    indexed_sentence = f"{index+1}. {sentence}"
    if isinstance(ctx, context.ApplicationContext):
        await ctx.respond(indexed_sentence)
    else:
        await ctx.send(indexed_sentence)
