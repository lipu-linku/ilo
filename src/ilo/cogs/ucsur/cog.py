# from pozzei

import re
from typing import Literal, cast

from discord import ApplicationContext, Bot
from discord.ext.commands import Cog

from ilo.cog_utils import Locale, load_file
from ilo.data import get_word_data
from ilo.strings import spoiler_text

vocab = cast(dict[str, str], load_file(__file__, "ucsur.json"))
chars = list(map(re.escape,list(vocab.keys())))
chars.sort(key=len,reverse=True)
    

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
        _ = await ctx.respond("Message is too long. Please try to keep messages below 500 characters.")
    string = clean_string(string)
    if not string:
        _ = await ctx.respond("Input became empty. Please provide a proper input.")
    
    response = re.sub("|".join(chars), lambda x: vocab[x.group(0)]+" " if vocab[x.group(0)][0] in "abcdefghijklmnopqrstuvwxyz" else vocab[x.group(0)], string) #the ternary adds a space after any latin word, which ucsur characters don't tend to have in-between

    # cleaning up:
    response = " ".join(response.split(" ")) #collapse all spaces to one
    response=re.sub("\u0020(?=[,\.:!\?\]\)<v\^>\+\-\&=_\|\}12345678　」])","",response)
    response=re.sub("\u0020(?=([　-〿]|[︀-️]|[󱤀-󱧿]|[←-↙]))","",response)
    
    _ = await ctx.respond(response,ephemeral=hide)

def clean_string(string: str): 
    clean_string = re.findall(r"([ -~]|[　-〿]|[︀-️]|[󱤀-󱧿]|[←-↙])", string)
    clean_string = "".join(clean_string)
    return clean_string
