from typing import Literal

import discord
from discord import ButtonStyle, Embed
from discord.ext.commands import Cog
from discord.ui import Button, View

from ilo import jasima
from ilo.cog_utils import Locale, load_file
from ilo.cogs.nimi.colour import colours
from ilo.preferences import Template, preferences



class CogNimi(Cog):
    def __init__(self, bot):
        self.bot = bot
        preferences.register(
            Template(
                self.locale, "language", "en", jasima.get_languages_for_slash_commands()
            )
        )
        preferences.register(
            Template(
                self.locale,
                "usage",
                "widespread",
                jasima.get_usages_for_slash_commands(),
            )
        )

    locale = Locale(__file__)

    @locale.command("nimi")
    @locale.option("nimi-word")
    async def slash_nimi(self, ctx, word):
        await nimi(ctx, word)

    @locale.command("n")
    @locale.option("n-word")
    async def slash_n(self, ctx, word):
        await nimi(ctx, word)

    # imo guess is a special case of nimi
    @locale.command("guess")
    @locale.option("guess-show", choices=["word", "def"])
    @locale.option("guess-usage", choices=jasima.USAGES)
    async def slash_guess(self, ctx, show: str = "def", usage: str = "widespread"):
        assert show in ("word", "def")
        await guess(ctx, show, usage)


async def nimi(ctx, word):
    lang = preferences.get(str(ctx.author.id), "language")

    response = jasima.get_word_entry(word)
    if isinstance(response, str):
        await ctx.respond(response)
        return
    embed = embed_response(word, lang, response, "concise")
    view = NimiView("expand", word, lang)
    await ctx.respond(embed=embed, view=view)


async def guess(ctx, show: Literal["word", "def"], usage: str):
    lang = preferences.get(str(ctx.author.id), "language")

    word, response = jasima.get_random_word(min_usage=usage)
    embed = guess_embed_response(word, lang, response, show)
    await ctx.respond(embed=embed)


def spoiler_wrap(s: str) -> str:
    return f"|| {s} ||"


def guess_embed_response(word, lang, response, show: Literal["word", "def"]):
    embed = Embed()
    embed.title = response["word"]
    if show != "word":
        embed.title = spoiler_wrap(embed.title)

    embed.colour = colours[response["usage_category"]]
    description = (
        response["def"][lang]
        if lang in response["def"]
        else "(en) {}".format(response["def"]["en"])
    )
    if show != "def":
        description = spoiler_wrap(description)
    embed.add_field(name="description", value=description)
    return embed


def embed_response(word, lang, response, embedtype):
    embed = Embed()
    embed.title = response["word"]
    embed.colour = colours[response["usage_category"]]
    description = (
        response["def"][lang]
        if lang in response["def"]
        else "(en) {}".format(response["def"]["en"])
    )
    usage = response["usage_category"] if "usage_category" in response else "unknown"
    embed.add_field(name="usage", value=f"{usage} ({response['book'].replace('none', 'no book')})")

    if embedtype == "concise":
        embed.add_field(name="description", value=description)

    if embedtype == "verbose":
        embed.add_field(name="description", value=description, inline=False)
        if "etymology" in response or "source_language" in response:
            embed.add_field(
                name="etymology", value=build_etymology(response), inline=False
            )
        if "ku_data" in response:
            embed.add_field(
                name="ku data",
                value="{} [(source)](http://tokipona.org/nimi_pu.txt)".format(
                    response["ku_data"]
                ),
                inline=False,
            )
        if "commentary" in response:
            embed.add_field(
                name="commentary", value=response["commentary"], inline=False
            )

    if response["book"] not in ("pu", "ku suli"):
        if "see_also" in response:
            embed.add_field(name="see also", value=response["see_also"])
    return embed


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
