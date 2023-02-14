import random

from discord.ext.commands import Cog

from ilo.cog_utils import Locale, load_file


class CogStest(Cog):
    def __init__(self, bot):
        self.bot = bot

    locale = Locale(__file__)

    @locale.command("stest")
    async def slash_stest(self, ctx):
        await stest(ctx)


async def stest(ctx):
    index, sentence = random.choice(list(enumerate(sentences)))
    indexed_sentence = f"{index+1}. {sentence}"
    await ctx.respond(indexed_sentence)


sentences = load_file(__file__, "sentences.txt")
