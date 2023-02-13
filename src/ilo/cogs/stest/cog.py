import random

from discord.ext.commands import Cog
from discord.commands import slash_command

from ilo.cog_utils import load_file
from ilo.defines import text


class CogStest(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="stest", description=text["DESC_STEST"])
    async def slash_stest(self, ctx):
        await stest(ctx)


async def stest(ctx):
    index, sentence = random.choice(list(enumerate(sentences)))
    indexed_sentence = f"{index+1}. {sentence}"
    await ctx.respond(indexed_sentence)


sentences = load_file(__file__, "sentences.txt")
