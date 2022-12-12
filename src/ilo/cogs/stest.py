from discord.ext import commands
from discord.commands import slash_command
from discord import Option

from ilo.defines import sentences
from ilo.defines import text
import random


class CogStest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="stest",
        description=text["DESC_STEST"],
    )
    async def slash_stest(self, ctx):
        await stest(ctx)


async def stest(ctx):
    index, sentence = random.choice(list(enumerate(sentences)))
    indexed_sentence = f"{index+1}. {sentence}"
    await ctx.respond(indexed_sentence)
