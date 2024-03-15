import io
import re
from typing import Literal, Tuple

from discord import File
from discord.commands.context import ApplicationContext
from discord.ext.commands import Cog

from ilo import sitelen
from ilo.cog_utils import Locale, font_autocomplete, handle_pref_error
from ilo.data import DEFAULT_FONT, SITELEN_SITELEN_FONT, USABLE_FONTS
from ilo.preferences import Template, preferences

VALID_STYLES = ["outline", "background"]
Style = Literal["outline"] | Literal["background"]


class CogSitelen(Cog):
    def __init__(self, bot):
        self.bot = bot
        preferences.register(
            Template(
                locale=self.locale,
                name="fontsize",
                default=72,
                validation=is_valid_fontsize,
            )
        )
        preferences.register(
            Template(
                locale=self.locale,
                name="color",
                default="ffffff",
                validation=is_valid_color,
            )
        )
        preferences.register(
            Template(
                locale=self.locale,
                name="font",
                default=DEFAULT_FONT,
                choices={font: font for font in USABLE_FONTS},
                validation=is_valid_font,
            )
        )
        preferences.register(
            Template(
                locale=self.locale,
                name="bgstyle",
                default="outline",
                choices={style: style for style in VALID_STYLES},
                validation=is_valid_bgstyle,
            )
        )

    locale = Locale(__file__)

    @locale.command("sp")
    @locale.option("sp-text")
    @locale.option("sp-font", autocomplete=font_autocomplete)
    @locale.option("sp-fontsize")
    @locale.option("sp-color")
    @locale.option("sp-bgstyle", choices=VALID_STYLES)
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
    @locale.option("sitelenpona-font", autocomplete=font_autocomplete)
    @locale.option("sitelenpona-fontsize")
    @locale.option("sitelenpona-color")
    @locale.option("sitelenpona-bgstyle", choices=VALID_STYLES)
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
    @locale.option("ss-bgstyle", choices=VALID_STYLES)
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
            ctx, text, SITELEN_SITELEN_FONT, fontsize, color, bgstyle, spoiler, hide
        )

    @locale.command("sitelensitelen")
    @locale.option("sitelensitelen-text")
    @locale.option("sitelensitelen-fontsize")
    @locale.option("sitelensitelen-color")
    @locale.option("sitelensitelen-bgstyle", choices=VALID_STYLES)
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
            ctx, text, SITELEN_SITELEN_FONT, fontsize, color, bgstyle, spoiler, hide
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
    bgstyle: Style = "outline",
    spoiler: bool = False,
    hide: bool = False,
):
    user_id = str(ctx.author.id)

    font = await handle_pref_error(ctx, user_id, "font", override=font)
    font = USABLE_FONTS[font]  # TODO: font from preferences isn't a usable font

    fontsize = await handle_pref_error(ctx, user_id, "fontsize", override=fontsize)
    color = await handle_pref_error(ctx, user_id, "color", override=color)

    bgstyle = await handle_pref_error(ctx, user_id, "bgstyle", override=bgstyle)

    text = unescape_newline(text)
    image = io.BytesIO(sitelen.display(text, font, fontsize, rgb_tuple(color), bgstyle))

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


def rgb_tuple(value: str) -> Tuple[int, int, int]:
    return tuple(bytes.fromhex(value))


def is_valid_font(value: str) -> bool:
    return value in USABLE_FONTS


def is_valid_fontsize(value: int) -> bool:
    return 14 <= value <= 500


def is_valid_color(value: str) -> bool:
    if re.match(r"^[0-9a-fA-F]{6}$", value):
        return True
    return False


def is_valid_bgstyle(style: Style) -> bool:
    return style in VALID_STYLES
