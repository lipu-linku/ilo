from discord.ext.commands import Cog

from discord import Embed
from discord import ButtonStyle
from discord.ui import View
from discord.ui import Button

from ilo.cog_utils import Locale, load_file
from ilo.preferences import preferences
from ilo.preferences import Template
from ilo import jasima

from ilo.cogs.nimi.colour import colours


class CogNimi(Cog):
    def __init__(self, bot):
        self.bot = bot
        preferences.register(Template(self.locale, "language", "en", jasima.get_languages_for_slash_commands()))

    locale = Locale(__file__)

    @locale.command("nimi")
    @locale.option("nimi-word")
    async def slash_nimi(self, ctx, word):
        await nimi(ctx, word)

    @locale.command("n")
    @locale.option("n-word")
    async def slash_n(self, ctx, word):
        await nimi(ctx, word)


async def nimi(ctx, word):
    lang = preferences.get(str(ctx.author.id), "language")

    response = jasima.get_word_entry(word)
    if isinstance(response, str):
        await ctx.respond(response)
        return
    embed = embed_response(word, lang, response, "concise")
    view = NimiView("expand", word, lang)
    await ctx.respond(embed=embed, view=view)


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
