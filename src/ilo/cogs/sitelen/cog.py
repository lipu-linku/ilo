import io
from discord.ext.commands import Cog
from discord import File

from ilo.cog_utils import Locale, load_file
from ilo.fonts import fonts
from ilo.preferences import preferences
from ilo.preferences import Template
from ilo import sitelen


class CogSitelen(Cog):
    def __init__(self, bot):
        self.bot = bot
        preferences.register(Template(self.locale, "fontsize", 72, validation=fontsize_validation))
        preferences.register(Template(self.locale, "color", "ffffff", validation=colour_validation))
        preferences.register(Template(self.locale, "font", "linja sike", {font: font for font in fonts}))

    locale = Locale(__file__)

    @locale.command("sp")
    @locale.option("sp-text")
    async def slash_sp(self, ctx, text):
        await sp(ctx, text)

    @locale.command("sitelenpona")
    @locale.option("sitelenpona-text")
    async def slash_sitelenpona(self, ctx, text):
        await sp(ctx, text)

    @locale.command("ss")
    @locale.option("ss-text")
    async def slash_ss(self, ctx, text):
        await ss(ctx, text)

    @locale.command("sitelensitelen")
    @locale.option("sitelensitelen-text")
    async def slash_sitelensitelen(self, ctx, text):
        await ss(ctx, text)

    @locale.command("preview")
    @locale.option("preview-text")
    async def slash_preview(self, ctx, text):
        await preview(ctx, text)


async def sp(ctx, text):
    fontsize = preferences.get(str(ctx.author.id), "fontsize")
    font = preferences.get(str(ctx.author.id), "font")
    color = preferences.get(str(ctx.author.id), "color")
    image = io.BytesIO(sitelen.display(text, fonts[font], fontsize, rgb_tuple(color)))
    await ctx.respond(file=File(image, filename="a.png"))


async def ss(ctx, text):
    fontsize = preferences.get(str(ctx.author.id), "fontsize")
    color = preferences.get(str(ctx.author.id), "color")
    font = "sitelen Latin (ss)"
    image = io.BytesIO(sitelen.display(text, fonts[font], fontsize, rgb_tuple(color)))
    await ctx.respond(file=File(image, filename="a.png"))


async def preview(ctx, text):
    fontsize = preferences.get(str(ctx.author.id), "fontsize")
    color = preferences.get(str(ctx.author.id), "color")
    images = []
    for font in fonts:
        images.append(sitelen.display(text, fonts[font], fontsize, rgb_tuple(color)))
    await ctx.respond(file=File(io.BytesIO(sitelen.stitch(images)), filename="a.png"))


def fontsize_validation(value):
    if not (value <= 500 and value >= 14):
        return "Font size is limited to the range from 14 to 500."
    return True


def colour_validation(value):
    if not is_colour(value):
        return "The string has to be a valid hexadecimal rgb colour, e.g. `2288ff`."
    return True


def is_colour(value):
    try:
        value = rgb_tuple(value)
        if len(value) == 3:
            return True
    except ValueError:
        return False


def rgb_tuple(value):
    return tuple(bytes.fromhex(value))
