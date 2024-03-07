from typing import Literal

from discord import ApplicationContext, ButtonStyle, Embed
from discord.ext.commands import Cog
from discord.ui import Button, View

from ilo import data, strings
from ilo.cog_utils import Locale, handle_pref_error, word_autocomplete
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
                validation=is_valid_language,
            )
        )
        preferences.register(
            Template(
                self.locale,
                "usage",
                "common",
                data.USAGES_FOR_PREFS,
                validation=is_valid_usage_category,
            )
        )

    locale = Locale(__file__)

    # @locale.option(
    #     "nimi-language",  # TODO: just make it available elsewhere
    #     autocomplete=build_autocomplete(
    #         preferences.templates["language"].choices.keys()
    #     ),
    # )
    @locale.command("nimi")
    @locale.option("nimi-query", autocomplete=word_autocomplete)
    @locale.option("nimi-hide")
    async def slash_nimi(self, ctx: ApplicationContext, query: str, hide: bool = True):
        await nimi(ctx, query, hide)

    @locale.command("n")
    @locale.option("n-query", autocomplete=word_autocomplete)
    @locale.option("n-hide")
    async def slash_n(self, ctx: ApplicationContext, query: str, hide: bool = True):
        await nimi(ctx, query, hide)

    # imo guess is a special case of nimi
    @locale.command("guess")
    @locale.option("guess-which", choices=["word", "def"])
    @locale.option("guess-hide")
    async def slash_guess(self, ctx, which: str = "def", hide: bool = True):
        assert which in ("word", "def")
        await guess(ctx, which, hide)


async def nimi(ctx: ApplicationContext, query: str, hide: bool = True):
    lang = await handle_pref_error(ctx, str(ctx.author.id), "language")

    success, response = strings.handle_word_query(query)
    if not success:
        await ctx.respond(response, ephemeral=True)
        return

    embed = embed_response(query, lang, response, "concise")
    view = NimiView("expand", query, lang)
    await ctx.respond(embed=embed, view=view, ephemeral=hide)
    # TODO: controllable ephemeral


async def guess(ctx, which: Literal["word", "def"], hide: bool = True):
    lang = await handle_pref_error(ctx, str(ctx.author.id), "language")
    usage = await handle_pref_error(ctx, str(ctx.author.id), "usage")

    word, response = data.get_random_word(min_usage=usage)
    embed = guess_embed_response(word, lang, response, which)
    await ctx.respond(embed=embed, ephemeral=hide)


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
    definition = data.deep_get(response, "translations", lang, "definition")
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
        embed.add_field(name="definition", value=definition)

    if embedtype == "verbose":
        embed.add_field(name="definition", value=definition, inline=False)
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

    if response["usage_category"] != "core":
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

        # for rname, link in word_data.get("resources", {}).items():
        word_data = data.get_word_data(word)
        link = deep_get(word_data, "resources", "sona_pona")
        if link:
            self.add_item(
                Button(
                    style=ButtonStyle.link,
                    label="sona.pona.la",
                    url=link,
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


def is_valid_language(value: str) -> bool:
    return value in data.LANGUAGE_DATA


def is_valid_usage_category(value: str) -> bool:
    return value in data.UsageCategory.__members__
