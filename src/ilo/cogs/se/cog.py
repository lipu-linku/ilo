# from pozzei

import re

from discord import ApplicationContext
from discord.ext.commands import Cog

from ilo.cog_utils import Locale, load_file
from ilo.data import get_word_data
from ilo.strings import spoiler_text


class CogSe(Cog):
    def __init__(self, bot):
        self.bot = bot

    locale = Locale(__file__)

    @locale.command("se")
    @locale.option("se-text")
    @locale.option("se-system", choices=["sitelen jelo","sitelen pilin"])
    @locale.option("se-spoiler")
    async def slash_se(self, ctx: ApplicationContext, text: str, system: str, spoiler: bool = False):
        await se(ctx, text, spoiler)


async def se(ctx: ApplicationContext, string: str, system: str, spoiler: bool = False):
    if len(string) > 500:
        response = (
            "Message is too long. Please try to keep messages below 500 characters."
        )
    string = clean_string(string)
    system = clean_string(system)
    if system=="sitelen pilin":
        chosen_system="sitelen_pilin"
    else:
        chosen_system="sitelen_jelo"

    if string == "":
        response = "Resulting string is empty. Please provide a proper input."

    response = " ".join(list(map(sitelen_emosi, [string.split(),chosen_system])))

    if spoiler:
        response = spoiler_text(response)
    await ctx.respond(response)


def clean_string(string: str):
    clean_string = re.findall(r"([a-zA-Z: .?!])", string)
    clean_string = "".join(clean_string)
    clean_string = re.sub(r"(:)+", " : ", clean_string)
    clean_string = re.sub(r"(\!)+", " ! ", clean_string)
    clean_string = re.sub(r"(\?)+", " ? ", clean_string)
    clean_string = re.sub(r"(\.){3,}", " … ", clean_string)
    clean_string = re.sub(r"(\.){1,2}", " . ", clean_string)
    clean_string = clean_string.lower()
    return clean_string


def sitelen_emosi(pref: list[list[str],str]):
    word=pref[0]
    chosen_system=pref[1]
    word_data = get_word_data(word)
    if word_data:
        if chosen_system=="sitelen_pilin":
            sitelen = word_data["representations"].get("sitelen_emosi")
        else:
            sitelen = word_data["representations"].get("sitelen_jelo")[0]
        if sitelen:
            return sitelen

    chars = []
    for letter in word:
        chars.append(extraemoji[letter])
    return " ".join(chars)


extraemoji = load_file(__file__, "extraemoji.json")
