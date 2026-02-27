import re

from discord import ApplicationContext, ButtonStyle, Colour, Embed
from discord.ext.commands import Cog
from discord.ui import Button, View

from ilo.cog_utils import Locale, build_autocomplete
from ilo.kemeka import load_kemeka_data, KemekaEntry

KEMEKA_ACCENT = Colour.from_rgb(80, 142, 0)


kemeka_data = load_kemeka_data()
kemeka_dict = {entry.keyword: entry for entry in kemeka_data}

kemeka_autocomplete = build_autocomplete([entry.keyword for entry in kemeka_data])


class CogKemeka(Cog):
    def __init__(self, bot):
        self.bot = bot

    locale = Locale(__file__)

    @locale.command("kemeka")
    @locale.option("kemeka-query", autocomplete=kemeka_autocomplete)
    @locale.option("kemeka-hide")
    async def slash_kemeka(
        self,
        ctx: ApplicationContext,
        query: str,
        hide: bool = False,
    ):
        await kemeka_command(ctx, query, hide)


async def kemeka_command(ctx: ApplicationContext, query: str, hide: bool):
    entry = kemeka_dict.get(query, None)
    if entry is None:
        await ctx.respond(
            f"The word you requested, ***{query}***, is not in *lipu Kemeka*. If the word was recently added, it may not have been updated in my database yet. If it's not in *lipu Kemeka* and you want it added, you can request it on [this form](https://docs.google.com/forms/d/e/1FAIpQLSclWsDweTAcnVr6rN4SVehxKqDtrvrEMC-IWT4vC29N22hl5g/viewform)!",
            ephemeral=True,
        )
        return

    embed = kemeka_embed(entry)
    view = KemekaView(word=query)
    await ctx.respond(embed=embed, view=view, ephemeral=hide)


def limit_len(entry: KemekaEntry, text: str, max_len: int) -> str:
    if len(text) <= max_len:
        return text
    return (
        text[: max_len - 32]
        + f"[\\[…\\]](https://kemeka.pona.la/?q={entry.keyword.replace(" ", "_")})"
    )


def kemeka_embed(entry: KemekaEntry) -> Embed:
    embed = Embed()

    embed.title = entry.keyword
    embed.colour = KEMEKA_ACCENT

    embed.description = entry.notes

    if entry.definitions:
        definition_text = []
        for i, definition in enumerate(entry.definitions):
            parts = []

            if len(entry.definitions) > 1:
                marker = definition.enumeration or str(i + 1)
                parts.append(f"**{marker}.**")

            eng = replace_md_links(definition.eng)
            tok = replace_md_links(definition.tok)
            parts.append(f"{eng} — **{tok}**")

            definition_line = " ".join(parts)
            definition_text.append(definition_line)

            if definition.examples:
                for example in definition.examples:
                    tok_ex = replace_md_links(example.tok)
                    eng_ex = replace_md_links(example.eng)
                    definition_text.append(f"> *{tok_ex}*")
                    definition_text.append(f"> \u00a0\u00a0\u00a0\u00a0{eng_ex}")
                definition_text.append("")

        full_text = "\n".join(definition_text)
        full_text = limit_len(entry, full_text, 2048)
        embed.description = full_text

    if entry.notes:
        notes_text = replace_md_links(entry.notes)
        notes_text = limit_len(entry, notes_text, 1024)

        embed.add_field(name="Notes", value=notes_text, inline=False)

    return embed


def replace_md_links(text: str) -> str:
    def link_replacer(match: re.Match) -> str:
        text = match.group(1)
        return f"[{text}](https://kemeka.pona.la/?q={text.replace(' ', '_')})"

    return re.sub(r"\[(.+?)\](?!\()", link_replacer, text)


class KemekaView(View):
    def __init__(self, word: str):
        super().__init__()
        self.add_item(
            Button(
                style=ButtonStyle.link,
                label="kemeka.pona.la",
                url=f"https://kemeka.pona.la/?q={word.replace(" ", "_")}",
            )
        )
