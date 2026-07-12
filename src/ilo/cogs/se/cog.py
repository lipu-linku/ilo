# from pozzei

import re
from typing import Literal, cast

from discord import ApplicationContext, Bot
from discord.ext.commands import Cog

from ilo.cog_utils import Locale, load_file
from ilo.data import Word
from ilo.strings import spoiler_text

UserChoices = Literal["sitelen jelo"] | Literal["sitelen pilin"]
LinkuEmojiReprs = Literal["sitelen_jelo"] | Literal["sitelen_emosi"]
choice_to_linku_repr: dict[UserChoices, LinkuEmojiReprs] = {
    "sitelen jelo": "sitelen_jelo",
    "sitelen pilin": "sitelen_emosi",
}


class CogSe(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    locale = Locale(__file__)

    @locale.command("se")
    @locale.option("se-text")
    @locale.option("se-system", choices=list(choice_to_linku_repr.keys()))
    @locale.option("se-spoiler")
    async def slash_se(
        self,
        ctx: ApplicationContext,
        text: str,
        system: str = "sitelen jelo",
        spoiler: bool = False,
    ):
        await se(ctx, text, cast(UserChoices, system), spoiler)


async def se(
    ctx: ApplicationContext, string: str, system: UserChoices, spoiler: bool = False
):
    if len(string) > 500:
        _ = await ctx.respond("Message is too long. Please try to keep messages below 500 characters.")
    string = clean_string(string)
    if not string:
        _ = await ctx.respond("Input became empty. Please provide a proper input.")

    chosen_system = choice_to_linku_repr[system]

    chars: list[str] = []
    for word in string.split():
        result = sitelen_emosi(word, chosen_system)
        chars.append(result)
    response = " ".join(chars)

    if spoiler:
        response = spoiler_text(response)
    _ = await ctx.respond(response)


def clean_string(string: str):
    clean_string = re.findall(r"([a-zA-Z: .?!])", string)
    clean_string = "".join(clean_string)
    clean_string = re.sub(r"(:)+", " : ", clean_string)
    clean_string = re.sub(r"(\!)+", " ! ", clean_string)
    clean_string = re.sub(r"(\?)+", " ? ", clean_string)
    clean_string = re.sub(r"(\.){3,}", " … ", clean_string)
    clean_string = re.sub(r"(\.){1,2}", " . ", clean_string)
    clean_string = clean_string.lower()
    return clean_string


def sitelen_emosi(word: Word, chosen_system: LinkuEmojiReprs) -> str:
    sitelen_ken: str | list[str] | None = word.representations.get(chosen_system)
    if not sitelen_ken:
        return fallback_emoji(word)

    if isinstance(sitelen_ken, list):
        # TODO: let user choose among the list
        sitelen_ken = sitelen_ken[0]

    return sitelen_ken


def fallback_emoji(word: Word) -> str:
    chars: list[str] = []
    for letter in word.string:
        chars.append(extraemoji[letter])
    return " ".join(chars)


extraemoji = cast(dict[str, str], load_file(__file__, "extraemoji.json"))
