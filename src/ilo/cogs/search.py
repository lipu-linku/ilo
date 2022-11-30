from discord import ButtonStyle, Embed, Option, context
from discord.commands import slash_command
from discord.ext import commands
from discord.ui import Button, View

from ilo import jasima
from ilo.cogs.nimi import embed_response
from ilo.colour import discord_colours
from ilo.defines import colours, text
from ilo.preferences import preferences


class CogNimi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name="search")
        async def command_search(ctx, search):
            if search.startswith("search:"):
                search = search.replace("search:", "", 1)
            await search(ctx, search)

    @slash_command(
        name="search",
        description=text["DESC_SEARCH"],
    )
    async def slash_search(self, ctx, word: Option(str, text["DESC_SEARCH_OPTION"])):
        await nimi(ctx, word)


async def search(ctx, word):
    lang = preferences.get(str(ctx.author.id), "language")

    response = jasima.get_word_entry(word)
    if isinstance(response, str):
        if isinstance(ctx, context.ApplicationContext):
            await ctx.respond(response)
        else:
            await ctx.send(response)
        return
    embed = embed_response(word, lang, response, "concise")
    view = NimiView("expand", word, lang)
    if isinstance(ctx, context.ApplicationContext):
        await ctx.respond(embed=embed, view=view)
    else:
        await ctx.send(embed=embed, view=view)


class NimiView(View):
    def __init__(self, buttontype, word, lang):
        super().__init__()
        minmax = NimiButton(
            style=ButtonStyle.primary,
            label=buttontype,
            custom_id=f"{buttontype};{word};{lang}",
        )
        self.add_item(minmax)
        url = "https://lipu-linku.github.io/?q={}".format(word)
        moreinfo = Button(style=ButtonStyle.link, label="more info", url=url)
        self.add_item(moreinfo)


class NimiButton(Button):
    async def callback(self, interaction):
        buttontype, word, lang = self.custom_id.split(";")
        if buttontype == "expand":
            embed = embed_response(word, lang, jasima.get_word_entry(word), "verbose")
            view = NimiView("minimise", word, lang)
        if buttontype == "minimise":
            embed = embed_response(word, lang, jasima.get_word_entry(word), "concise")
            view = NimiView("expand", word, lang)
        await interaction.response.edit_message(embed=embed, view=view)


def build_etymology(response):
    etymology = "←"
    if "source_language" in response:
        etymology += " " + response["source_language"]
    if "etymology" in response:
        etymology += " " + response["etymology"]
    return etymology
