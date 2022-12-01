import random

from discord import Option, context, option
from discord.commands import slash_command
from discord.ext import commands

from ilo.defines import prompts, text


class CogPrompt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name="prompt")
        async def command_prompt(ctx, lang):
            await prompt(ctx, lang)

    @slash_command(
        name="prompt",
        description=text["DESC_PROMPT"],
    )
    @option(
        name="lang",
        description=text["DESC_PROMPT_LANGUAGE_OPTION"],
        choices=["en", "tok"],
        # required=True,
        default="tok",
    )
    async def slash_prompt(
            self, ctx, lang: str
    ):
        await prompt(ctx, lang)


async def prompt(ctx, lang: str):
    if isinstance(ctx, context.ApplicationContext):
        callback = ctx.respond
    else:
        callback = ctx.send
    to_fetch = prompts[lang]
    sentence = random.choice(to_fetch)
    await callback(sentence)
