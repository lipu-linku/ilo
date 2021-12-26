from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord import Option
from discord import OptionChoice

from defines import acro_choices
from defines import fonts
from defines import text

from jasima import get_languages_for_slash_commands
import preferences

def to_choices(dictionary):
    return [OptionChoice(name=k, value=v) for k, v in dictionary.items()]

language_choices = to_choices(get_languages_for_slash_commands())

class CogPreferences(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    prefs = SlashCommandGroup(
        "preferences",
        text["DESC_PREFS"]
        )

    @prefs.command(
        name="fontsize",
        description=text["DESC_PREFS_FONTSIZE"],
        )
    async def preferences_fontsize(self, ctx, size: Option(int, text["DESC_PREFS_FONTSIZE_OPTION"])):
        if not (size <= 500 and size >= 14):
            await ctx.respond("Font size is limited to the range from 14 to 500.")
        else:
            preferences.set_preference(str(ctx.author.id), "fontsize", size)
            await ctx.respond("Set fontsize preference for **{}** to **{}**.".format(ctx.author.display_name, size))


    @prefs.command(
        name="acro",
        description=text["DESC_PREFS_ACRO"],
        )
    async def preferences_acro(self, ctx, book: Option(str, text["DESC_PREFS_ACRO_OPTION"], choices=to_choices(acro_choices))):
        preferences.set_preference(str(ctx.author.id), "acro", book)
        await ctx.respond("Set acronym book preference for **{}** to **{}**.".format(ctx.author.display_name, book))

    @prefs.command(
        name="font",
        description=text["DESC_PREFS_FONT"],
        )
    async def preferences_font(self, ctx, font: Option(str, text["DESC_PREFS_FONT_OPTION"], choices=list(fonts))):
        preferences.set_preference(str(ctx.author.id), "font", font)
        await ctx.respond("Set font preference for **{}** to **{}**.".format(ctx.author.display_name, font))

    @prefs.command(
        name="reset",
        description=text["DESC_PREFS_RESET"],
        )
    async def preferences_reset(self, ctx):
        preferences.reset_preferences(str(ctx.author.id))
        await ctx.respond("Reset preferences for **{}**.".format(ctx.author.display_name))

    @prefs.command(
        name="language",
        description=text["DESC_PREFS_LANGUAGE"],
        )
    async def preferences_language(self, ctx, lang: Option(str, text["DESC_PREFS_LANGUAGE_OPTION"], choices=language_choices)):
        preferences.set_preference(str(ctx.author.id), "language", lang)
        await ctx.respond("Set language preference for **{}** to **{}**.".format(ctx.author.display_name, lang))


