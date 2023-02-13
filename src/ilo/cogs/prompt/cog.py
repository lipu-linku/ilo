import random

from discord.ext.commands import Cog
from discord.commands import slash_command, option

from ilo.cog_utils import load_file
from ilo.defines import text
from ilo.preferences import preferences


class CogPrompt(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="prompt", description=text["DESC_PROMPT"])
    @option(
        name="translate",
        description=text["DESC_PROMPT_LANGUAGE_OPTION"],
        default=True # choices are implied
    )
    async def slash_prompt(self, ctx, translate: bool):
        await prompt(ctx, translate)


async def prompt(ctx, translate: bool):
    all_sents = random.choice(prompts)
    tok_prompt = all_sents["tok"]

    # if user lang is tok, don't translate
    lang = preferences.get(str(ctx.author.id), "language")
    translate = translate and (lang != "tok")
    if translate:
        translation = all_sents[lang] if lang in all_sents else all_sents["en"]
        tok_prompt  += f"\n||{translation}||"
    await ctx.respond(tok_prompt)


prompts = load_file(__file__, "prompts.json")
