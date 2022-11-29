from discord.ext import commands
from discord.commands import slash_command
from discord import Option

from discord import context

from ilo.defines import borgle_map
from ilo.defines import text
import re

class CogBorgle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name="borgle")
        async def command_borgle(ctx, *, text):
            if text.startswith("text:"):
                text = text.replace("text:", "", 1)
            await borgle(ctx, text)

        @bot.command(name="deborgle")
        async def command_deborgle(ctx, *, text):
            if text.startswith("text:"):
                text = text.replace("text:", "", 1)
            await deborgle(ctx, text)

    @slash_command(
      name='borgle',
      description=text["DESC_BORGLE"],
    )
    async def slash_borgle(self, ctx, text: Option(str, text["DESC_BORGLE_OPTION"])):
        await borgle(ctx, text)

    @slash_command(
      name='deborgle',
      description=text["DESC_DEBORGLE"],
    )
    async def slash_deborgle(self, ctx, text: Option(str, text["DESC_DEBORGLE_OPTION"])):
        await deborgle(ctx, text)


async def borgle(ctx, text):
    if isinstance(ctx, context.ApplicationContext):
        await ctx.respond(do_text(text))
    else:
        await ctx.send(do_text(text))

async def deborgle(ctx, text):
    if isinstance(ctx, context.ApplicationContext):
        await ctx.respond(undo(text))
    else:
        await ctx.send(undo(text))


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

