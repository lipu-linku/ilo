from typing import Literal

from discord import ButtonStyle, Embed
from discord.ext.commands import Cog
from discord.ui import Button, View

from ilo import data, strings
from ilo.cog_utils import Locale, word_autocomplete
from ilo.cogs.nimi.colour import colours
from ilo.data import deep_get
from ilo.preferences import Template, preferences


class CogNimi(Cog):
    def __init__(self, bot):
        self.bot = bot
        preferences.register(
            Template(
                self.locale,
                "language",
                "en",
                data.LANGUAGES_FOR_PREFS,
                validation=language_validation,
            )
        )
        preferences.register(
            Template(
                self.locale,
                "usage",
                "widespread",
                data.USAGES_FOR_PREFS,
                validation=usage_validation,
            )
        )

    locale = Locale(__file__)

    @locale.command("nimi")
    @locale.option("nimi-word", autocomplete=word_autocomplete)
    async def slash_nimi(self, ctx, word):
        await nimi(ctx, word)

    @locale.command("n")
    @locale.option("n-word", autocomplete=word_autocomplete)
    async def slash_n(self, ctx, word):
        await nimi(ctx, word)

    # imo guess is a special case of nimi
    @locale.command("guess")
    @locale.option("guess-hide", choices=["word", "def"])
    async def slash_guess(self, ctx, hide: str = "def"):
        assert hide in ("word", "def")
        await guess(ctx, hide)


async def nimi(ctx, word):
    lang = preferences.get(str(ctx.author.id), "language")

    success, response = strings.handle_word_query(word)
    if not success:
        await ctx.respond(response)
        return
    embed = embed_response(word, lang, response, "concise")
    view = NimiView("expand", word, lang)
    await ctx.respond(embed=embed, view=view)


async def guess(ctx, hide: Literal["word", "def"]):
    lang = preferences.get(str(ctx.author.id), "language")
    usage = preferences.get(str(ctx.author.id), "usage")
    # assert usage in data.USAGES

    word, response = data.get_random_word(min_usage=usage)
    embed = guess_embed_response(word, lang, response, hide)
    await ctx.respond(embed=embed)


def spoiler_wrap(s: str) -> str:
    return f"|| {s} ||"


def guess_embed_response(word: str, lang: str, response, hide: Literal["word", "def"]):
    embed = Embed()
    embed.title = response["word"]
    if hide == "word":
        embed.title = spoiler_wrap(embed.title)

    embed.colour = colours[response["usage_category"]]
    definition = deep_get(response, "translations", lang, "definition")

    if hide == "def":
        definition = spoiler_wrap(definition)
    embed.add_field(name="definition", value=definition)
    return embed


def embed_response(
    word: str,
    lang: str,
    response,
    embedtype: Literal["concise", "verbose"],
):
    embed = Embed()
    embed.title = response["word"]
    embed.colour = colours[response.get("usage_category", "obscure")]
    description = data.deep_get(response, "translations", lang, "definition")
    # TODO: REPLACEME with `definition`
    usage = response["usage_category"] if "usage_category" in response else "unknown"
    embed.add_field(
        name="usage", value=f"{usage} ({response['book'].replace('none', 'no book')})"
    )

    embed.set_thumbnail(
        url=f"https://raw.githubusercontent.com/lipu-linku/ijo/main/sitelenpona/sitelen-seli-kiwen/{word}.png",
    )
    # embed.set_thumbnail( # TODO: not final, but REPLACEME
    #     url=data.deep_get(response, "representations", "sitelen_pona_svg", 0)
    # )

    if embedtype == "concise":
        embed.add_field(name="description", value=description)

    if embedtype == "verbose":
        embed.add_field(name="description", value=description, inline=False)
        etym_untrans = response.get("etymology")
        etym_trans = data.deep_get(response, "translations", lang, "etymology")
        if etym_untrans and etym_trans:
            embed.add_field(
                name="etymology",
                value=strings.format_etymology(etym_untrans, etym_trans),
                inline=False,
            )
        if "ku_data" in response:
            embed.add_field(
                name="ku data",
                value="{}\n[(source one)](http://tokipona.org/nimi_pu.txt), [(source two)](http://tokipona.org/nimi_pi_pu_ala.txt)".format(
                    strings.format_ku_data(response["ku_data"])
                ),
                inline=False,
            )
        commentary = data.deep_get(response, "translations", lang, "commentary")
        if commentary:
            embed.add_field(name="commentary", value=commentary, inline=False)

    if response["usage_category"] not in ("core", "widespread"):
        # these words may have `see_also` but don't need it
        if "see_also" in response:
            embed.add_field(name="see also", value=", ".join(response["see_also"]))
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
        self.add_item(
            Button(
                style=ButtonStyle.link,
                label="linku.la",
                url=f"https://linku.la/?q={word}",
                # url=f"https://linku.la/words/{word}",
            )
        )
        self.add_item(
            Button(
                style=ButtonStyle.link, label="nimi.li", url=f"https://nimi.li/{word}"
            )
        )

        word_data = data.get_word_data(word)
        if sonapona_link := data.deep_get(word_data, "resources", "sona_pona"):
            self.add_item(
                Button(
                    style=ButtonStyle.link,
                    label="sona.pona.la",
                    url=sonapona_link,
                )
            )


class NimiButton(Button):
    async def callback(self, interaction):
        buttontype, word, lang = self.custom_id.split(";")
        if buttontype == "expand":
            embed = embed_response(word, lang, data.get_word_data(word), "verbose")
            view = NimiView("minimise", word, lang)
        elif buttontype == "minimise":
            embed = embed_response(word, lang, data.get_word_data(word), "concise")
            view = NimiView("expand", word, lang)
        else:
            await interaction.response.edit_message("Something went wrong!")
            return
        await interaction.response.edit_message(embed=embed, view=view)


def language_validation(value: str) -> bool | str:
    return value in data.LANGUAGE_DATA or "Selected language not available."


def usage_validation(value: str) -> bool | str:
    return value in data.Usage.__members__ or "Selected usage not valid."
