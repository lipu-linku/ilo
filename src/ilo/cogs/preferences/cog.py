import re

from discord import AutocompleteContext, Option, OptionChoice
from discord.commands import SlashCommandGroup
from discord.ext.commands import Cog

from ilo.cog_utils import Locale, startswith_filter
from ilo.preferences import preferences

CHOICE_SIZE = 25

RESPONSES = {
    "set": "{key}: **{value}** (default: {default})\n",
    "invalid": "{key}: {value}. The value is invalid, **{default}** (default) is used instead.\n",
    "unset": "{key}: {default} (by default)\n",
}


def build_subcommands(prefs, template):
    autocompleter = build_autocomplete(template.choices) if template.choices else None
    option = Option(
        template.option_type,
        template.option_desc,
        autocomplete=autocompleter,
    )
    build_subcommand(prefs, template.name, template.description, option)


def build_subcommand(prefs, name, description, option):
    @prefs.command(name=name, description=description)
    async def preference_subcommand(self, ctx, preference: option):
        template = preferences.templates[re.sub(r"_page\d*", "", ctx.command.name)]
        if template.choices and isinstance(
            template.choices, dict
        ):  # must be before validation
            preference = template.choices.get(preference)

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


def build_autocomplete(options: list[str]):
    def autocompleter(ctx: AutocompleteContext):
        return startswith_filter(ctx.value.lower(), options)

    return autocompleter


async def prefs_autocomplete(ctx: AutocompleteContext):
    return startswith_filter(ctx.value.lower(), preferences.templates.keys())


class CogPreferences(Cog):
    def __init__(self, bot):
        self.bot = bot
        # for template in preferences.templates.values():
        #    self.build_subcommands(template, prefs)
        # for subcommand in prefs.subcommands:
        #    print(subcommand)

    locale = Locale(__file__)

    prefs = SlashCommandGroup("preferences", locale["prefs"])
    for template in preferences.templates.values():
        build_subcommands(prefs, template)

    @prefs.command(
        name="list",
        description=locale["list"],
    )
    async def list(self, ctx):
        response = "Preferences for **{}**:\n".format(ctx.author.display_name)
        for key in preferences.templates:
            value = preferences.get_raw(str(ctx.author.id), key)
            status = preferences.get_status(str(ctx.author.id), key, value)
            default = preferences.get_default(key)
            response += RESPONSES[status].format(key=key, value=value, default=default)
        await ctx.respond(response)

    @prefs.command(
        name="reset",
        description=locale["reset"],
    )
    async def reset(self, ctx):
        preferences.reset(str(ctx.author.id))
        await ctx.respond(
            "Reset all preferences for **{}**.".format(ctx.author.display_name)
        )

    @prefs.command(name="show", description=locale["show"])
    async def show(
        self,
        ctx,
        preference: Option(str, name="preference", autocomplete=prefs_autocomplete),
    ):
        if template := preferences.templates.get(preference):
            if c := template.choices:  # we know it's a dict
                await ctx.respond(format_opts(c.keys()), ephemeral=True)
            else:
                await ctx.respond("No specific for that preference", ephemeral=True)
                # TODO: some of them are open ended like font size and color
            return
        await ctx.respond("That preference doesn't exist.", ephemeral=True)


def format_opts(opts: list):
    return "\n".join(opts)
