# from pozzei

import re

from discord.ext import commands
from discord.commands import slash_command
from discord import Option

from discord import context

from ilo.defines import text
from ilo.jasima import sitelen_emosi


class CogSe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name="se")
        async def command_se(ctx, *, text):
            if text.startswith("text:"):
                text = text.replace("text:", "", 1)
            await se(ctx, text)

    @slash_command(
        name="se",
        description=text["DESC_SE"],
    )
    async def slash_se(self, ctx, text: Option(str, text["DESC_SE_OPTION"])):
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
    if isinstance(ctx, context.ApplicationContext):
        await ctx.respond(response)
    else:
        await ctx.send(response)


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
