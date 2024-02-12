# from pozzei

import re

from discord.ext.commands import Cog

from ilo.cog_utils import Locale, load_file
from ilo.data import get_word_data


class CogSe(Cog):
    def __init__(self, bot):
        self.bot = bot

    locale = Locale(__file__)

    @locale.command("se")
    @locale.option("se-text")
    async def slash_se(self, ctx, text):
        await se(ctx, text)


async def se(ctx, string):
    if len(string) > 500:
        response = (
            "Message is too long. Please try to keep messages below 500 characters."
        )
    string = clean_string(string)

    if string == "":
        response = "Resulting string is empty. Please provide a proper input."

    response = " ".join(list(map(sitelen_emosi, string.split())))
    await ctx.respond(response)


def clean_string(string):
    clean_string = re.findall(r"([a-zA-Z: .?!])", string)
    clean_string = "".join(clean_string)
    clean_string = re.sub(r"(:)+", " : ", clean_string)
    clean_string = re.sub(r"(\!)+", " ! ", clean_string)
    clean_string = re.sub(r"(\?)+", " ? ", clean_string)
    clean_string = re.sub(r"(\.){3,}", " … ", clean_string)
    clean_string = re.sub(r"(\.){1,2}", " . ", clean_string)
    clean_string = clean_string.lower()
    return clean_string


def sitelen_emosi(word: str):
    word_data = get_word_data(word)
    if word_data:
        sitelen = word_data["representations"].get("sitelen_emosi")
        if sitelen:
            return sitelen

    chars = []
    for letter in word:
        chars.append(extraemoji[letter])
    return " ".join(chars)


extraemoji = load_file(__file__, "extraemoji.json")
