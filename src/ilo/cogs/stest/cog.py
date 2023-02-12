from pathlib import Path
import random

from discord.ext import commands
from discord.commands import slash_command
from discord import Option

from ilo.defines import text

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


with open(Path(__file__).parent / "sentences.txt", encoding="utf-8") as f:
     sentences = list(f.readlines())
