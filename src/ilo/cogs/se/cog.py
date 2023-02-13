# from pozzei

import re

from discord.ext.commands import Cog
from discord.commands import slash_command, option

from ilo.cog_utils import load_file
from ilo.defines import text
from ilo.jasima import bundle


class CogSe(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="se", description=text["DESC_SE"])
    @option(name="text", description=text["DESC_SE_OPTION"])
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


def sitelen_emosi(word):
    entries = bundle["data"]
    if word in entries:
        if "sitelen_emosi" in entries[word]:
            return entries[word]["sitelen_emosi"]
    chars = []
    for letter in word:
        chars.append(extraemoji[letter])
    return " ".join(chars)


extraemoji = load_file(__file__, "extraemoji.json")
