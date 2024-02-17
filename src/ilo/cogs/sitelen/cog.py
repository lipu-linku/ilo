import io
from typing import Optional, Tuple

from discord import File
from discord.commands.context import ApplicationContext
from discord.ext.commands import Cog

from ilo import sitelen
from ilo.cog_utils import Locale, font_autocomplete
from ilo.data import DEFAULT_FONT, SITELEN_SITELEN_FONT, USABLE_FONTS
from ilo.preferences import Template, preferences


class CogSitelen(Cog):
    def __init__(self, bot):
        self.bot = bot
        preferences.register(
            Template(self.locale, "fontsize", 72, validation=fontsize_validation)
        )
        preferences.register(
            Template(self.locale, "color", "ffffff", validation=colour_validation)
        )
        preferences.register(
            Template(
                self.locale,
                "font",
                DEFAULT_FONT,
                {font: font for font in USABLE_FONTS},
                validation=font_validation,
            )
        )

    locale = Locale(__file__)

    @locale.command("sp")
    @locale.option("sp-text")
    @locale.option("sp-font", autocomplete=font_autocomplete)
    async def slash_sp(self, ctx: ApplicationContext, text: str, font: str = ""):
        await sp(ctx, text, font)

    @locale.command("sitelenpona")
    @locale.option("sitelenpona-text")
    @locale.option("sitelenpona-font", autocomplete=font_autocomplete)
    async def slash_sitelenpona(
        self, ctx: ApplicationContext, text: str, font: str = ""
    ):
        await sp(ctx, text, font)

    @locale.command("ss")
    @locale.option("ss-text")
    async def slash_ss(self, ctx: ApplicationContext, text: str):
        await ss(ctx, text)

    @locale.command("sitelensitelen")
    @locale.option("sitelensitelen-text")
    async def slash_sitelensitelen(self, ctx: ApplicationContext, text: str):
        await ss(ctx, text)


def unescape_newline(text: str) -> str:
    return text.replace("\\n", "\n")


async def sp(ctx: ApplicationContext, text: str, font: str = ""):
    fontsize = preferences.get(str(ctx.author.id), "fontsize")
    font = font or preferences.get(str(ctx.author.id), "font")
    color = preferences.get(str(ctx.author.id), "color")
    text = unescape_newline(text)
    image = io.BytesIO(
        sitelen.display(text, USABLE_FONTS[font], fontsize, rgb_tuple(color))
    )
    await ctx.respond(file=File(image, filename="a.png"))


async def ss(ctx: ApplicationContext, text: str):
    fontsize = preferences.get(str(ctx.author.id), "fontsize")
    color = preferences.get(str(ctx.author.id), "color")
    font = SITELEN_SITELEN_FONT
    text = unescape_newline(text)
    image = io.BytesIO(
        sitelen.display(text, USABLE_FONTS[font], fontsize, rgb_tuple(color))
    )
    await ctx.respond(file=File(image, filename="a.png"))


def fontsize_validation(value: int) -> bool | str:
    if not (value <= 500 and value >= 14):
        return "Font size is limited to the range from 14 to 500."
    return True


def colour_validation(value: int) -> bool | str:
    if not is_colour(value):
        return "The string has to be a valid hexadecimal rgb colour, e.g. `2288ff`."
    return True


def font_validation(value: str) -> bool | str:
    return value in USABLE_FONTS or "Invalid font selected."


def is_colour(value) -> Optional[bool]:
    try:
        value = rgb_tuple(value)
        if len(value) == 3:
            return True
    except ValueError:
        return False


def rgb_tuple(value) -> Tuple[int, int, int]:
    return tuple(bytes.fromhex(value))
