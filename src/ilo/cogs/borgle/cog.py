import re

from discord import ApplicationContext
from discord.ext.commands import Cog

from ilo.cog_utils import Locale, load_file
from ilo.strings import spoiler_text


class CogBorgle(Cog):
    def __init__(self, bot):
        self.bot = bot

    locale = Locale(__file__)

    @locale.command("borgle")
    @locale.option("borgle-text")
    @locale.option("borgle-spoiler")
    async def slash_borgle(
        self,
        ctx: ApplicationContext,
        text: str,
        spoiler: bool = False,
    ):
        borgled_text = do_text(text)
        if spoiler:
            borgled_text = spoiler_text(borgled_text)
        await ctx.respond(borgled_text)

    @locale.command("deborgle")
    @locale.option("deborgle-text")
    @locale.option("deborgle-spoiler")
    async def slash_deborgle(
        self,
        ctx: ApplicationContext,
        text: str,
        spoiler: bool = False,
    ):
        deborgled_text = undo(text)
        if spoiler:
            deborgled_text = spoiler_text(deborgled_text)
        await ctx.respond(deborgled_text)


def do_text(text: str):
    return "\n".join(do_line(line) for line in text.split("\n"))


def do_line(line: str):
    return " ".join(do_word(word) for word in line.split())


def do_word(word: str):
    # coda n
    word = re.sub(r"(?<=[aeiou])n(?![aeiou])", "q", word)
    # sorry yupekosi
    word = word.replace("y", "j")
    # word final unstressed i
    word = re.sub(r"(?<!\b[^aeiou])i(?=\b)", "y", word)
    # plorcly borglar
    return "".join(do_letter(letter) for letter in word)


def do_letter(letter: str):
    if letter not in borgle_map:
        return letter
    else:
        return borgle_map[letter]


def undo(text: str):
    for key, value in borgle_map.items():
        text = re.sub(f"(?<!@){value}", f"@{key}", text)
    return text.replace("q", "n").replace("y", "i").replace("@", "")


borgle_map = load_file(__file__, "borgle_map.json")
