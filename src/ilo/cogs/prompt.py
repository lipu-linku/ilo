import random

from discord import context, option
from discord.commands import slash_command
from discord.ext import commands

from ilo.preferences import preferences
from ilo.defines import prompts, text


class CogPrompt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name="prompt")
        async def command_prompt(ctx, translate: bool):
            await prompt(ctx, translate)

    @slash_command(
        name="prompt",
        description=text["DESC_PROMPT"],
    )
    @option(
        name="translate",
        description=text["DESC_PROMPT_LANGUAGE_OPTION"],
        default=True # choices are implied
    )
    async def slash_prompt(self, ctx, translate: bool):
        await prompt(ctx, translate)


async def prompt(ctx, translate: bool):
    if isinstance(ctx, context.ApplicationContext):
        callback = ctx.respond
    else:
        callback = ctx.send
    all_sents = random.choice(prompts)
    tok_prompt = all_sents["tok"]

    # if user lang is tok, don't translate
    lang = preferences.get(str(ctx.author.id), "language")
    translate = translate and (lang != "tok")
    if translate:
        translation = all_sents[lang] if lang in all_sents else all_sents["en"]
        tok_prompt  += f"\n||{translation}||"
    await callback(tok_prompt)
