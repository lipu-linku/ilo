from typing import Literal

from discord import ApplicationContext, ButtonStyle, Embed
from discord.ext.commands import Cog
from discord.ui import Button, View

from ilo import cog_utils as utils
from ilo import data, strings
from ilo.cogs.nimi.colour import colours
from ilo.preferences import Template, preferences
from ilo.word import Word

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
    @locale.option("nimi-sandbox")
    @locale.option("nimi-language", autocomplete=language_autocomplete)
    @locale.option("nimi-hide")
    async def slash_nimi(
        self,
        ctx: ApplicationContext,
        query: str,
        sandbox: bool = False,
        language: str = "",
        hide: bool = False,
    ):
        await nimi(ctx, query, sandbox, language, hide)

    @locale.command("n")
    @locale.option("n-query", autocomplete=utils.word_autocomplete)
    @locale.option("n-sandbox")
    @locale.option("n-language", autocomplete=language_autocomplete)
    @locale.option("n-hide")
    async def slash_n(
        self,
        ctx: ApplicationContext,
        query: str,
        sandbox: bool = False,
        language: str = "",
        hide: bool = False,
    ):
        await nimi(ctx, query, sandbox, language, hide)

    # imo guess is a special case of nimi
    @locale.command("guess")
    @locale.option("guess-which", choices=["word", "def"])
    @locale.option("guess-language", autocomplete=language_autocomplete)
    @locale.option("guess-hide")
    async def slash_guess(
        self,
        ctx: ApplicationContext,
        which: str = "def",
        language: str = "",
        hide: bool = False,
    ):
        assert which in ("word", "def")
        await guess(ctx, which, language, hide)


async def nimi(
    ctx: ApplicationContext,
    query: str,
    sandbox: bool = False,
    language: str = "",
    hide: bool = False,
):
    # this feeds user's mistake back when we fail to find
    language = data.LANGUAGES_FOR_PREFS.get(language, language)
    lang = await utils.handle_pref_error(ctx, str(ctx.author.id), "language", language)

    success, resp = strings.handle_word_query(query, sandbox)

    if not success:
        await ctx.respond(resp, ephemeral=True)
        return

    await data.fetch_lang_and_defer(lang, ctx, hide)
    embed = embed_response(resp, lang, "concise")
    view = NimiView("expand", resp, lang)
    await ctx.respond(embed=embed, view=view, ephemeral=hide)
    # TODO: controllable ephemeral


async def guess(
    ctx, which: Literal["word", "def"], language: str = "", hide: bool = True
):
    language = data.LANGUAGES_FOR_PREFS.get(language, language)
    lang = await utils.handle_pref_error(ctx, str(ctx.author.id), "language", language)

    usage = await utils.handle_pref_error(ctx, str(ctx.author.id), "usage")
    word = data.get_random_word(min_usage=usage)

    await data.fetch_lang_and_defer(lang, ctx, hide)
    embed = guess_embed_response(word, lang, which)
    await ctx.respond(embed=embed, ephemeral=hide)


def spoiler_wrap(s: str) -> str:
    return f"|| {s} ||"


def guess_embed_response(word: Word, lang: str, hide: Literal["word", "def"]):
    embed = Embed()
    embed.title = word.string
    if hide == "word":
        embed.title = spoiler_wrap(embed.title)

    embed.colour = colours[word.usage_category]
    definition = word.get_definition(lang)

    if hide == "def":
        definition = spoiler_wrap(definition)
    embed.add_field(name="definition", value=definition)
    return embed


def embed_response(
    word: Word,
    lang: str,
    embedtype: Literal["concise", "verbose"],
):
    embed = Embed()
    embed.title = word.string
    embed.colour = colours[word.usage_category]
    embed.add_field(
        name="usage", value=f"{word.usage_category} ({word.book.replace('none', 'no book')})"
    )

    embed.set_thumbnail(url=word.image)

    inline = embedtype == "concise"
    embed.add_field(name="definition", value=word.get_definition(lang), inline=inline)

    if embedtype == "verbose":
        etym = word.get_etymology(lang).replace("; ", "\n")
        if etym:
            embed.add_field(
                name="etymology",
                value=etym,
                inline=inline,
            )
        if word.ku_data:
            embed.add_field(
                name="ku data",
                value="{}\n[(source one)](http://tokipona.org/nimi_pu.txt), [(source two)](http://tokipona.org/nimi_pi_pu_ala.txt)".format(
                    strings.format_ku_data(word.ku_data)
                ),
                inline=inline,
            )
        commentary = word.get_commentary(lang)
        if commentary:
            embed.add_field(name="commentary", value=commentary, inline=inline)

    if word.usage_category != "core" and word.see_also:
        embed.add_field(
            name="see also", value=", ".join(word.see_also), inline=inline
        )
    if word.usage_category == "uncommon":
        embed.set_footer(
            text="⚠️ This word is uncommon. Many speakers don't use this word."
        )
    elif word.usage_category == "obscure":
        embed.set_footer(
            text="⚠️ This word is obscure. Most speakers don't use or understand this word."
        )
    elif word.usage_category == "sandbox":
        embed.set_footer(
            text="⚠️ This proposed word is in the sandbox. It is not in use by the community."
        )
    return embed


class NimiView(View):
    def __init__(self, buttontype: str, word: Word, lang: str):
        super().__init__()
        minmax = NimiButton(
            style=ButtonStyle.primary,
            label=buttontype,
            custom_id=f"{buttontype};{word.ID};{lang}",
        )
        self.add_item(minmax)
        self.add_item(
            Button(
                style=ButtonStyle.link,
                label="linku.la",
                url=f"https://linku.la/words/{word.ID}"
            )
        )
        self.add_item(
            Button(
                style=ButtonStyle.link, label="nimi.li", url=f"https://nimi.li/{word.ID}"
            )
        )

        link = word.resources["sona_pona"]
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
        buttontype, word_str, lang = self.custom_id.split(";")
        word: Word = data.get_word(word_str)
        if buttontype == "expand":
            embed = embed_response(word, lang, "verbose")
            view = NimiView("minimise", word, lang)
        elif buttontype == "minimise":
            embed = embed_response(word, lang, "concise")
            view = NimiView("expand", word, lang)
        else:
            await interaction.response.edit_message("Something went wrong!")
            return
        await interaction.response.edit_message(embed=embed, view=view)
