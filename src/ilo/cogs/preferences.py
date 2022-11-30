import re

from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord import Option
from discord import OptionChoice

from ilo.defines import text
from ilo.defines import pref_list

from ilo.preferences import preferences

CHOICE_SIZE = 25


def to_choices(dictionary):
    return [OptionChoice(name=k, value=v) for k, v in dictionary.items()]


def to_chunks(sequence, n):
    return [sequence[i : i + n] for i in range(0, len(sequence), n)]


def build_subcommands(prefs, template):
    if template.choices is None:
        option = Option(template.option_type, template.option_desc)
        build_subcommand(prefs, template.name, template.description, option)
    else:
        choices = to_chunks(to_choices(template.choices), CHOICE_SIZE)
        for index, chunk in enumerate(choices):
            option = Option(template.option_type, template.option_desc, choices=chunk)
            name = (
                f"{template.name}_page{index+1}" if len(choices) > 1 else template.name
            )
            build_subcommand(prefs, name, template.description, option)


def build_subcommand(prefs, name, description, option):
    @prefs.command(name=name, description=description)
    async def preference_subcommand(self, ctx, preference: option):
        template = preferences.templates[re.sub("_page\d*", "", ctx.command.name)]
        validation = template.validation(preference)
        if validation is not True:
            await ctx.respond(validation)
            return
        preferences.set(str(ctx.author.id), template.name, preference)
        await ctx.respond(
            "Set {} preference for **{}** to **{}**.".format(
                template.name, ctx.author.display_name, preference
            )
        )


class CogPreferences(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # for template in preferences.templates.values():
        #    self.build_subcommands(template, prefs)
        # for subcommand in prefs.subcommands:
        #    print(subcommand)

    prefs = SlashCommandGroup("preferences", text["DESC_PREFS"])
    for template in preferences.templates.values():
        build_subcommands(prefs, template)

    @prefs.command(
        name="list",
        description=text["DESC_PREFS_LIST"],
    )
    async def list(self, ctx):
        response = "Preferences for **{}**:\n".format(ctx.author.display_name)
        for key in preferences.templates:
            value = preferences.get_raw(str(ctx.author.id), key)
            status = preferences.get_status(str(ctx.author.id), key, value)
            default = preferences.get_default(key)
            response += pref_list[status].format(key=key, value=value, default=default)
        await ctx.respond(response)

    @prefs.command(
        name="reset",
        description=text["DESC_PREFS_RESET"],
    )
    async def reset(self, ctx):
        preferences.reset(str(ctx.author.id))
        await ctx.respond(
            "Reset all preferences for **{}**.".format(ctx.author.display_name)
        )
