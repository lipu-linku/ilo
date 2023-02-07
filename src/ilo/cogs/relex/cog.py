from discord import option
from discord.commands import slash_command
from discord.ext import commands

from ilo.defines import text
from ilo.preferences import preferences
from ilo.relexer import relex


def setup(bot):
    bot.add_cog(CogRelex(bot))


class CogRelex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="relex", description=text["DESC_RELEX"])
    @option(name="input", description=text["DESC_RELEX_INPUT"])
    # @option(
    #     name="lang",
    #     description=text["DESC_RELEX_LANGUAGE_OPTION"],
    #     # choices=get_languages_for_slash_commands(),
    #     default="",
    # )
    async def slash_relex(self, ctx, input):  # , lang):
        await relex_command(ctx, input)  # , lang)


async def relex_command(ctx, input: str):  # , lang: Optional[str]):
    # TODO: re-add lang option when more langs are available?
    # lang = preferences.get(str(ctx.author.id), "language") if not lang else lang
    # lang = "en" if lang == "tok" else lang
    # coalesce to 1. param lang 2. preferences lang 3. not tok 4. en default

    lang = "en"
    relexed = relex(input, lang)

    await ctx.respond(relexed)
