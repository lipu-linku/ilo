# from pozzei

import logging
from typing import Any

from discord import ApplicationContext, Bot, Message
from discord.commands import message_command
from discord.ext.commands import Cog

from ilo.cog_utils import Locale
from ilo.ucsur import ucsur_replace

LOG = logging.getLogger("ilo")


class CogUcsur(Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        super().__init__()

    locale = Locale(__file__)

    @locale.command("ucsur")
    @locale.option("ucsur-text")
    @locale.option("ucsur-hide", choices=[True, False])
    async def slash_ucsur(
        self,
        ctx: ApplicationContext,
        text: str,
        hide: bool = False,
    ):
        await ucsur(ctx, text, hide)

    @message_command(name="Convert UCSUR")
    async def appmenu_ucsur(self, ctx: ApplicationContext, message: Message):
        await ucsur(ctx, message.content, hide=True)


async def ucsur(ctx: ApplicationContext, string: str, hide: bool = False):
    if len(string) > 500:
        _ = await ctx.respond(
            "Message is too long. Please try to keep messages below 500 characters."
        )

    if not string:
        _ = await ctx.respond("Input became empty. Please provide a proper input.")

    response = ucsur_replace(string)

    if not response:
        _ = await ctx.respond("Input became empty. Please provide a proper input.")

    _ = await ctx.respond(response, ephemeral=hide)
