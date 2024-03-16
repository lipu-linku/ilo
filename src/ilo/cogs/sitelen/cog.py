import io

from discord import File
from discord.commands.context import ApplicationContext
from discord.ext.commands import Cog

from ilo import cog_utils as utils
from ilo import data, sitelen
from ilo.preferences import Template, preferences


class CogSitelen(Cog):
    def __init__(self, bot):
        self.bot = bot
        preferences.register(
            Template(
                locale=self.locale,
                name="fontsize",
                default=data.DEFAULT_FONTSIZE,
                validation=utils.is_valid_fontsize,
            )
        )
        preferences.register(
            Template(
                locale=self.locale,
                name="color",
                default=data.DEFAULT_COLOR,
                validation=utils.is_valid_color,
            )
        )
        preferences.register(
            Template(
                locale=self.locale,
                name="font",
                default=data.DEFAULT_FONT,
                choices={font: font for font in data.USABLE_FONTS},
                validation=utils.is_valid_font,
            )
        )

        # FIXME: This will require breaking font preferences.
        # Font data is stored by font name, what the user enters.
        # But font names and directories/filenames are not necessarily static.
        # Users should still select fonts by name, but we should store the font id.
        # For comparison, languages already do this.
        # In the nimi cog, we pass data.LANGUAGES_FOR_PREFS- no dict comprehension.
        # NOTE: In the preferences list command, the user currently sees the langcode
        # instead of the language name. For fonts, they see the font name because we
        # store it. This should be fixed.

        preferences.register(
            Template(
                locale=self.locale,
                name="bgstyle",
                default=data.DEFAULT_BGSTYLE,
                choices={style: style for style in utils.VALID_STYLES},
                validation=utils.is_valid_bgstyle,
            )
        )

    locale = utils.Locale(__file__)

    @locale.command("sp")
    @locale.option("sp-text")
    @locale.option("sp-font", autocomplete=utils.font_autocomplete)
    @locale.option("sp-fontsize")
    @locale.option("sp-color")
    @locale.option("sp-bgstyle", choices=utils.VALID_STYLES)
    @locale.option("sp-spoiler")
    @locale.option("sp-hide")
    async def slash_sp(
        self,
        ctx: ApplicationContext,
        text: str,
        font: str = "",
        fontsize: int = 0,
        color: str = "",
        bgstyle: str = "",
        spoiler: bool = False,
        hide: bool = False,
    ):
        await sp(ctx, text, font, fontsize, color, bgstyle, spoiler, hide)

    @locale.command("sitelenpona")
    @locale.option("sitelenpona-text")
    @locale.option("sitelenpona-font", autocomplete=utils.font_autocomplete)
    @locale.option("sitelenpona-fontsize")
    @locale.option("sitelenpona-color")
    @locale.option("sitelenpona-bgstyle", choices=utils.VALID_STYLES)
    @locale.option("sitelenpona-spoiler")
    @locale.option("sitelenpona-hide")
    async def slash_sitelenpona(
        self,
        ctx: ApplicationContext,
        text: str,
        font: str = "",
        fontsize: int = 0,
        color: str = "",
        bgstyle: str = "",
        spoiler: bool = False,
        hide: bool = False,
    ):
        await sp(ctx, text, font, fontsize, color, bgstyle, spoiler, hide)

    @locale.command("ss")
    @locale.option("ss-text")
    @locale.option("ss-fontsize")
    @locale.option("ss-color")
    @locale.option("ss-bgstyle", choices=utils.VALID_STYLES)
    @locale.option("ss-spoiler")
    @locale.option("ss-hide")
    async def slash_ss(
        self,
        ctx: ApplicationContext,
        text: str,
        fontsize: int = 0,
        color: str = "",
        bgstyle: str = "",
        spoiler: bool = False,
        hide: bool = False,
    ):
        await sp(
            ctx,
            text,
            data.SITELEN_SITELEN_FONT,
            fontsize,
            color,
            bgstyle,
            spoiler,
            hide,
        )

    @locale.command("sitelensitelen")
    @locale.option("sitelensitelen-text")
    @locale.option("sitelensitelen-fontsize")
    @locale.option("sitelensitelen-color")
    @locale.option("sitelensitelen-bgstyle", choices=utils.VALID_STYLES)
    @locale.option("sitelensitelen-spoiler")
    @locale.option("sitelensitelen-hide")
    async def slash_sitelensitelen(
        self,
        ctx: ApplicationContext,
        text: str,
        fontsize: int = 0,
        color: str = "",
        bgstyle: str = "",
        spoiler: bool = False,
        hide: bool = False,
    ):
        await sp(
            ctx,
            text,
            data.SITELEN_SITELEN_FONT,
            fontsize,
            color,
            bgstyle,
            spoiler,
            hide,
        )


def unescape_newline(text: str) -> str:
    return text.replace("\\n", "\n")


def text_to_filename(text: str) -> str:
    text = text.lower()
    text = text.replace(" ", "_")
    text = "".join(char for char in text if char.isalnum() or char == "_")

    text = text[:50]
    # NOTE: this is a semi-arbitrary practical-for-enduser thing
    return text


async def sp(
    ctx: ApplicationContext,
    text: str,
    font: str = "",
    fontsize: int = 0,
    color: str = "",
    bgstyle: str = "",
    spoiler: bool = False,
    hide: bool = False,
):
    user_id = str(ctx.author.id)

    font = await utils.handle_pref_error(ctx, user_id, "font", override=font)
    font = data.USABLE_FONTS[font]  # TODO: font from preferences isn't a usable font

    fontsize = await utils.handle_pref_error(
        ctx, user_id, "fontsize", override=fontsize
    )
    color = await utils.handle_pref_error(ctx, user_id, "color", override=color)
    bgstyle = await utils.handle_pref_error(ctx, user_id, "bgstyle", override=bgstyle)

    text = unescape_newline(text)
    image = io.BytesIO(
        sitelen.display(text, font, fontsize, utils.rgb_tuple(color), bgstyle)
    )

    alt_text = f"{ctx.author.display_name} said: {text}"
    filename = text_to_filename(text) + ".png"
    await ctx.respond(
        file=File(
            fp=image,
            filename=filename,
            description=alt_text,
            spoiler=spoiler,
        ),
        ephemeral=hide,
    )
