import re

from discord.ext.commands import Cog
from discord.commands import slash_command, option

from ilo.cog_utils import load_file
from ilo.defines import text


class CogBorgle(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="borgle", description=text["DESC_BORGLE"])
    @option(name="text", description=text["DESC_BORGLE_OPTION"])
    async def slash_borgle(self, ctx, text):
        await ctx.respond(do_text(text))

    @slash_command(name="deborgle", description=text["DESC_DEBORGLE"])
    @option(name="text", description=text["DESC_DEBORGLE_OPTION"])
    async def slash_deborgle(self, ctx, text):
        await ctx.respond(undo(text))


def do_text(text):
    return "\n".join(do_line(line) for line in text.split("\n"))


def do_line(line):
    return " ".join(do_word(word) for word in line.split())


def do_word(word):
    # coda n
    word = re.sub(r"(?<=[aeiou])n(?![aeiou])", "q", word)
    # sorry yupekosi
    word = word.replace("y", "j")
    # word final unstressed i
    word = re.sub(r"(?<!\b[^aeiou])i(?=\b)", "y", word)
    # plorcly borglar
    return "".join(do_letter(letter) for letter in word)


def do_letter(letter):
    if letter not in borgle_map:
        return letter
    else:
        return borgle_map[letter]


def undo(text):
    for key, value in borgle_map.items():
        text = re.sub(f"(?<!@){value}", f"@{key}", text)
    return text.replace("q", "n").replace("y", "i").replace("@", "")


borgle_map = load_file(__file__, "borgle_map.json")
