import random

from discord import context, option
from discord.commands import slash_command
from discord.ext import commands

from ilo.defines import get_languages_for_prompts, prompts, text


class CogPrompt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name="prompt")
        async def command_prompt(ctx, lang):
            await prompt(ctx, lang)

    available_langs = get_languages_for_prompts()

    @slash_command(
        name="prompt",
        description=text["DESC_PROMPT"],
    )
    @option(
        name="lang",
        description=text["DESC_PROMPT_LANGUAGE_OPTION"],
        choices=available_langs,
        # required=True,
        default=available_langs[0],  # assumed to be tok
    )
    async def slash_prompt(self, ctx, lang: str):
        await prompt(ctx, lang)


async def prompt(ctx, lang: str):
    if isinstance(ctx, context.ApplicationContext):
        callback = ctx.respond
    else:
        callback = ctx.send
    all_sents = random.choice(prompts)
    sentence = all_sents[lang]
    await callback(sentence)
