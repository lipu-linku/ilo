import io
import logging

from discord import Bot, File, Message, Thread
from discord.commands.context import ApplicationContext
from discord.ext.commands import Cog

from ilo import cog_utils as utils
from ilo import data, sitelen
from ilo.preferences import Template, preferences
from ilo.strings import rm_refs
from ilo.ucsur import ucsur_replace
from ilo.webhook import WebhookManager, WebhookResult

LOG = logging.getLogger("ilo")
ERRORS = {
    None: "Something went wrong, and I'm not sure what! Please notify the Linku developers.",
    WebhookResult.DMChannel: "Couldn't make a webhook! Webhooks are not supported in DMs.",
    WebhookResult.NoPermission: "Couldn't make a webhook! Please have an admin check my permissions.",
}


class CogSitelen(Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot: Bot = bot
        self.webhooks: WebhookManager = WebhookManager(bot)
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
        preferences.register(
            Template(
                locale=self.locale,
                name="proxy",
                default=data.DEFAULT_PROXY,
                validation=lambda x: isinstance(x, bool),
            )
        )
        preferences.register(
            Template(
                locale=self.locale,
                name="linewrap",
                default=data.DEFAULT_LINE_WRAP,
                validation=lambda x: isinstance(x, bool),
            )
        )
        preferences.register(
            Template(
                locale=self.locale,
                name="linewidth",
                default=data.DEFAULT_LINE_WIDTH,
                validation=utils.is_valid_line_width,
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
    # @locale.option("sp-proxy")
    @locale.option("sp-convert")
    @locale.option("sp-linewrap")
    @locale.option("sp-linewidth")

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
        # proxy: bool = False,
        convert: bool = False,
        linewrap: bool = False,
        linewidth: int = 0
    ):
        await self.sp(
            ctx,
            text,
            font,
            fontsize,
            color,
            bgstyle,
            spoiler,
            hide,
            # proxy,
            convert,
            linewrap,
            linewidth
        )

    @locale.command("sitelenpona")
    @locale.option("sitelenpona-text")
    @locale.option("sitelenpona-font", autocomplete=utils.font_autocomplete)
    @locale.option("sitelenpona-fontsize")
    @locale.option("sitelenpona-color")
    @locale.option("sitelenpona-bgstyle", choices=utils.VALID_STYLES)
    @locale.option("sitelenpona-spoiler")
    @locale.option("sitelenpona-hide")
    # @locale.option("sitelenpona-proxy")
    @locale.option("sitelenpona-convert")
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
        # proxy: bool = False,
        convert: bool = False,
        linewrap: bool = False,
        linewidth: int = 0
    ):
        await self.sp(
            ctx,
            text,
            font,
            fontsize,
            color,
            bgstyle,
            spoiler,
            hide,
            # proxy,
            convert,
            linewrap,
            linewidth
        )

    @locale.command("ss")
    @locale.option("ss-text")
    @locale.option("ss-fontsize")
    @locale.option("ss-color")
    @locale.option("ss-bgstyle", choices=utils.VALID_STYLES)
    @locale.option("ss-spoiler")
    @locale.option("ss-hide")
    # @locale.option("ss-proxy")
    async def slash_ss(
        self,
        ctx: ApplicationContext,
        text: str,
        font: str = "",
        fontsize: int = 0,
        color: str = "",
        bgstyle: str = "",
        spoiler: bool = False,
        hide: bool = False,
        # proxy: bool = False,
        linewrap: bool = False,
        linewidth: int = 0
    ):
        await self.sp(
            ctx,
            text,
            data.SITELEN_SITELEN_FONT,
            fontsize,
            color,
            bgstyle,
            spoiler,
            hide,
            # proxy,
            False,
            linewrap,
            linewidth
        )

    @locale.command("sitelensitelen")
    @locale.option("sitelensitelen-text")
    @locale.option("sitelensitelen-fontsize")
    @locale.option("sitelensitelen-color")
    @locale.option("sitelensitelen-bgstyle", choices=utils.VALID_STYLES)
    @locale.option("sitelensitelen-spoiler")
    @locale.option("sitelensitelen-hide")
    # @locale.option("sitelensitelen-proxy")
    async def slash_sitelensitelen(
        self,
        ctx: ApplicationContext,
        text: str,
        font: str = "",
        fontsize: int = 0,
        color: str = "",
        bgstyle: str = "",
        spoiler: bool = False,
        hide: bool = False,
        # proxy: bool = False,
        linewrap: bool = False,
        linewidth: int = 0
    ):
        await self.sp(
            ctx,
            text,
            data.SITELEN_SITELEN_FONT,
            fontsize,
            color,
            bgstyle,
            spoiler,
            hide,
            # proxy,
            False,
            linewrap,
            linewidth
        )

    async def make_sp_reply(
        self,
        ctx: ApplicationContext,
        text: str,
        font: str = "",
        fontsize: int = 0,
        color: str = "",
        bgstyle: str = "",
        spoiler: bool = False,
        convert: bool = False,
        linewrap: bool = False,
        linewidth: int = 0
    ) -> tuple[File, list[str]]:
        user_id = str(ctx.author.id)

        # TODO: font from preferences isn't a usable font
        font = await utils.handle_pref_error(ctx, user_id, "font", font)
        font = data.USABLE_FONTS[font]

        fontsize = await utils.handle_pref_error(ctx, user_id, "fontsize", fontsize)
        color = await utils.handle_pref_error(ctx, user_id, "color", color)
        bgstyle = await utils.handle_pref_error(ctx, user_id, "bgstyle", bgstyle)
        linewrap = await utils.handle_pref_error(ctx, user_id, "linewrap", linewrap)
        linewidth = await utils.handle_pref_error(ctx, user_id, "linewidth", linewidth)
        # TODO: get channel name or user display name?
        # we can't stop them from getting smooshed in the render process...
        text, refs = rm_refs(text)
        # alt_text = f"{ctx.author.display_name} said: {text}"
        alt_text = text
        # we want to make alt text from the original text in case the changes are destructive
        # but mentions are an exception since they're a kinda useless ID otherwise

        if convert:
            text = ucsur_replace(text)
        text = unescape_newline(text)
        # desktop alt text has no newlines
        image = io.BytesIO(
            sitelen.display(text, font, fontsize, utils.rgb_tuple(color), bgstyle, linewrap, linewidth)
        )
        filename = text_to_filename(text) + ".png"
        file = File(
            fp=image,
            filename=filename,
            description=alt_text,
            spoiler=spoiler,
        )
        return file, refs

    async def handle_proxy(self, msg: Message):
        pass

    async def sp(
        self,
        ctx: ApplicationContext,
        text: str,
        font: str = "",
        fontsize: int = 0,
        color: str = "",
        bgstyle: str = "",
        spoiler: bool = False,
        hide: bool = False,
        convert: bool = False,
        linewrap: bool = False,
        linewidth: int = 0
    ):
        user_id = str(ctx.author.id)
        proxy = await utils.handle_pref_error(ctx, user_id, "proxy", False)
        await ctx.defer(ephemeral=hide)

        kwargs = {}
        file, refs = await self.make_sp_reply(
            ctx,
            text,
            font,
            fontsize,
            color,
            bgstyle,
            spoiler,
            convert,
            linewrap,
            linewidth
        )

        kwargs["file"] = file
        if refs:  # will be mentions, then channels
            kwargs["content"] = " ".join(refs)

        sent = None
        if proxy and not hide:
            channel = ctx.channel
            if isinstance(channel, Thread):
                kwargs["thread"] = channel
                channel = ctx.channel.parent

            kwargs["username"] = ctx.author.display_name
            kwargs["avatar_url"] = ctx.author.display_avatar.url

            sent = await self.webhooks.send(ctx, channel, **kwargs)
            if sent:
                await ctx.delete()
                return
            kwargs.pop("username")
            kwargs.pop("avatar_url")
            kwargs.pop("thread") if kwargs.get("thread") else None

        LOG.info("%s %s", kwargs, hide)
        _ = await ctx.respond(**kwargs, ephemeral=hide)
        if proxy and not hide and not sent:
            # suppress dm error reporting
            _ = (
                await ctx.respond(ERRORS[sent], ephemeral=True)
                if sent != WebhookResult.DMChannel
                else None
            )


def unescape_newline(text: str) -> str:
    return text.replace("\\n", "\n")


def text_to_filename(text: str) -> str:
    # NOTE: We do NOT support UCSUR filenames.
    # Maybe in the future when we make an UCSUR converter?
    text = text.lower()
    text = text.replace(" ", "_")
    text = "".join(char for char in text if char.isalnum() or char == "_")

    text = text[:50]
    # NOTE: this is a semi-arbitrary practical-for-enduser thing

    if not text:
        # if we replace all text
        text = "image"
    return text
