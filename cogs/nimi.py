from discord.ext import commands
from discord.commands import slash_command
from discord import Option
from discord import Embed
from discord import ButtonStyle
from discord.ui import View
from discord.ui import Button

from discord import context

from defines import text
from defines import colours
from preferences import preferences
from colour import discord_colours
import jasima

class CogNimi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name="nimi")
        async def command_nimi(ctx, word):
            if word.startswith("word:"):
                word = word.replace("word:", "", 1)
            await nimi(ctx, word)
        @bot.command(name="n")
        async def command_n(ctx, word):
            if word.startswith("word:"):
                word = word.replace("word:", "", 1)
            await nimi(ctx, word)

    @slash_command(
      name='nimi',
      description=text["DESC_NIMI"],
    )
    async def slash_nimi(self, ctx, word: Option(str, text["DESC_NIMI_OPTION"])):
        await nimi(ctx, word)

    @slash_command(
      name='n',
      description=text["DESC_NIMI"],
    )
    async def slash_n(self, ctx, word: Option(str, text["DESC_NIMI_OPTION"])):
        await nimi(ctx, word)

async def nimi(ctx, word):
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

def embed_response(word, lang, response, embedtype):
    embed = Embed()
    embed.title = response["word"]
    embed.colour = discord_colours(colours)[response["book"]]
    description = response["def"][lang] if lang in response["def"] else "(en) {}".format(response["def"]["en"])
    embed.add_field(name="book", value=response["book"])

    if embedtype == "concise":
        embed.add_field(name="description", value=description)

    if embedtype == "verbose":
        embed.add_field(name="description", value=description, inline=False)
        if "etymology" in response or "source_language" in response:
            embed.add_field(name="etymology", value=build_etymology(response), inline=False)
        if "ku_data" in response:
            embed.add_field(name="ku data", value="{} [(source)](http://tokipona.org/nimi_pu.txt)".format(response["ku_data"]), inline=False)
        if "commentary" in response:
            embed.add_field(name="commentary", value=response["commentary"], inline=False)

    if response["book"] not in ("pu", "ku suli"):
        if "see_also" in response:
            embed.add_field(name="see also", value=response["see_also"])
    return embed


class NimiView(View):
    def __init__(self, buttontype, word, lang):
        super().__init__()
        minmax = NimiButton(style=ButtonStyle.primary,
                            label=buttontype,
                            custom_id=f"{buttontype};{word};{lang}")
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
