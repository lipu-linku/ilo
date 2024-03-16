from discord.ext.commands import Cog

from ilo.cog_utils import Locale, handle_pref_error
from ilo.cogs.acro import acronym
from ilo.preferences import Template, preferences


class CogAcro(Cog):
    def __init__(self, bot):
        self.bot = bot
        preferences.register(Template(self.locale, "acro", "ku suli", acro_choices))

    locale = Locale(__file__)

    @locale.command("acro")
    @locale.option("acro-text")
    async def slash_acro(self, ctx, text):
        await acro(ctx, text)


async def acro(ctx, text):
    book = await handle_pref_error(ctx, str(ctx.author.id), "acro")
    await ctx.respond(acronym.respond(text, book))


acro_choices = {
    "only pu words": "pu",
    "pu and ku suli words": "ku suli",
    "all pu, ku suli and ku lili words": "ku lili",
    "all words": "all",
}
