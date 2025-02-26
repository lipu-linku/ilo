# from pozzei

import re
from typing import Literal, cast

from discord import ApplicationContext, Bot
from discord.ext.commands import Cog

from ilo.cog_utils import Locale, load_file
from ilo.data import get_word_data
from ilo.strings import spoiler_text

vocab = cast(dict[str, str], load_file(__file__, "ucsur.json"))

class CogSe(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    locale = Locale(__file__)

    @locale.command("ucsur")
    @locale.option("ucsur-text")
    @locale.option("se-hide", choices=[True,False])
    async def slash_ucsur(
        self,
        ctx: ApplicationContext,
        text: str,
        hide: bool = False,
    ):
        await ucsur(ctx, text, hide)

async def ucsur(
  ctx: ApplicationContext, string: str, hide: bool = False
):
    if len(string) > 500:
        response = (
            "Message is too long. Please try to keep messages below 500 characters."
        )
    string = clean_string(string)
    if not string:
        _ = await ctx.respond("Input became empty. Please provide a proper input.")
    # TODO: convert string with vocab
    _ = await ctx.respond(response,ephemeral=hide)

def clean_string(string: str): #TODO: figure out what needs to be cleaned
  clean_string=string
  return clean_string
