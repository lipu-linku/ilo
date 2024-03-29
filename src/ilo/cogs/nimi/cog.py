from typing import Literal

from discord import ApplicationContext, ButtonStyle, Embed
from discord.ext.commands import Cog
from discord.ui import Button, View

from ilo import cog_utils as utils
from ilo import data, strings
from ilo.cogs.nimi.colour import colours
from ilo.preferences import Template, preferences

language_autocomplete = utils.build_autocomplete(data.LANGUAGES_FOR_PREFS)


class CogNimi(Cog):
    def __init__(self, bot):
        self.bot = bot
        preferences.register(
            Template(
                locale=self.locale,
                name="language",
                default=data.DEFAULT_LANGUAGE,
                choices=data.LANGUAGES_FOR_PREFS,
                validation=utils.is_valid_language,
            )
        )

        preferences.register(
            Template(
                self.locale,
                "usage",
                data.DEFAULT_USAGE_CATEGORY,
                data.USAGES_FOR_PREFS,
                validation=utils.is_valid_usage_category,
            )
        )

    locale = utils.Locale(__file__)

    @locale.command("nimi")
    @locale.option("nimi-query", autocomplete=utils.word_autocomplete)
    @locale.option("nimi-language", autocomplete=language_autocomplete)
    @locale.option("nimi-hide")
    async def slash_nimi(
        self, ctx: ApplicationContext, query: str, language: str = "", hide: bool = True
    ):
        await nimi(ctx, query, language, hide)

    @locale.command("n")
    @locale.option("n-query", autocomplete=utils.word_autocomplete)
    @locale.option("n-language", autocomplete=language_autocomplete)
    @locale.option("n-hide")
    async def slash_n(
        self, ctx: ApplicationContext, query: str, language: str = "", hide: bool = True
    ):
        await nimi(ctx, query, language, hide)

    # imo guess is a special case of nimi
    @locale.command("guess")
    @locale.option("guess-which", choices=["word", "def"])
    @locale.option("guess-language", autocomplete=language_autocomplete)
    @locale.option("guess-hide")
    async def slash_guess(
        self, ctx, which: str = "def", language: str = "", hide: bool = True
    ):
        assert which in ("word", "def")
        await guess(ctx, which, language, hide)


async def nimi(
    ctx: ApplicationContext, query: str, language: str = "", hide: bool = True
):
    # this feeds user's mistake back when we fail to find
    language = data.LANGUAGES_FOR_PREFS.get(language, language)
    lang = await utils.handle_pref_error(ctx, str(ctx.author.id), "language", language)

    success, response = strings.handle_word_query(query)
    if not success:
        await ctx.respond(response, ephemeral=True)
        return

    embed = embed_response(query, lang, response, "concise")
    view = NimiView("expand", query, lang)
    await ctx.respond(embed=embed, view=view, ephemeral=hide)
    # TODO: controllable ephemeral


async def guess(
    ctx, which: Literal["word", "def"], language: str = "", hide: bool = True
):
    language = data.LANGUAGES_FOR_PREFS.get(language, language)
    lang = await utils.handle_pref_error(ctx, str(ctx.author.id), "language", language)
    usage = await utils.handle_pref_error(ctx, str(ctx.author.id), "usage")

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
    definition = data.deep_get(response, "translations", lang, "definition")

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

    inline = embedtype == "concise"
    embed.add_field(name="definition", value=definition, inline=inline)

    if embedtype == "verbose":
        etym_untrans = response.get("etymology")
        etym_trans = data.deep_get(response, "translations", lang, "etymology")
        if etym_untrans and etym_trans:
            embed.add_field(
                name="etymology",
                value=strings.format_etymology(etym_untrans, etym_trans),
                inline=inline,
            )
        if "ku_data" in response:
            embed.add_field(
                name="ku data",
                value="{}\n[(source one)](http://tokipona.org/nimi_pu.txt), [(source two)](http://tokipona.org/nimi_pi_pu_ala.txt)".format(
                    strings.format_ku_data(response["ku_data"])
                ),
                inline=inline,
            )
        commentary = data.deep_get(response, "translations", lang, "commentary")
        if commentary:
            embed.add_field(name="commentary", value=commentary, inline=inline)

    if response["usage_category"] != "core":
        # these words may have `see_also` but don't need it
        if "see_also" in response:
            embed.add_field(
                name="see also", value=", ".join(response["see_also"]), inline=inline
            )
    if response["usage_category"] == "uncommon":
        embed.set_footer(
            text="⚠️ This word is uncommon. Many speakers don't use this word."
        )
    elif response["usage_category"] == "obscure":
        embed.set_footer(
            text="⚠️ This word is obscure. Most speakers don't use or understand this word."
        )
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
        link = data.deep_get(word_data, "resources", "sona_pona")
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
