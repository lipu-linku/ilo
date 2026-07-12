import logging
import re
from datetime import datetime
from itertools import zip_longest
from typing import Any, Callable, Dict, Literal, cast

from discord import Embed, Message
from sonatoki.Preprocessors import DiscordChannels, DiscordMentions

from ilo import data
from ilo.cog_utils import load_file
from ilo.data import Word

LOG = logging.getLogger()

STRINGS = cast(dict[str, str], load_file(__file__, "locale.json"))

MAX_EMBED_SIZE = 900
# this is to fly under the requirement
CLIPPED_EMBED_SIZE = 750


### coalescing to human readable response
def __coalesce_resp(
    query: str,
    searchfunc: Callable[[str], Any],
    *args: list[Any],
    **kwargs: dict[Any, Any],
) -> tuple[Literal[True], Word] | tuple[Literal[False], str]:
    if len(query.split()) > 1:
        return False, STRINGS["multiple_words"].format(query)

    resp = searchfunc(query, *args, **kwargs)
    if not resp:
        return False, STRINGS["missing_word"].format(query)
    return True, resp


def handle_word_query(
    query: str,
    sandbox: bool = False,
) -> tuple[Literal[True], Word] | tuple[Literal[False], str]:
    if len(query.split()) > 1:
        return False, STRINGS["multiple_words"].format(query)

    resp = data.get_non_sandbox_word(query)
    if resp:
        return True, resp

    sandbox_resp = data.get_sandbox_word(query)
    if sandbox and sandbox_resp:
        return True, sandbox_resp
    if sandbox_resp:
        return False, STRINGS["sandbox_word"].format(query)

    return False, STRINGS["missing_word"].format(query)


def handle_sign_query(
    query: str,
) -> tuple[Literal[True], Word] | tuple[Literal[False], str]:
    return __coalesce_resp(query, data.get_lukapona_data)


### formatting


def clip_for_embed(to_embed: str):
    if len(to_embed) > MAX_EMBED_SIZE:
        to_embed = to_embed[:CLIPPED_EMBED_SIZE]
        to_embed += "…"
    return to_embed


def format_ku_data(ku_data: Dict[str, int]):
    """Take linku's ku data and format it like Sonja's ku data"""
    sorted_data = sorted(ku_data.items(), key=lambda x: x[1], reverse=True)
    to_format = []
    for word, score in sorted_data:
        to_format.append(f"{word}: {score}%")
    formatted = ", ".join(to_format)
    print(len(formatted))
    print(formatted)
    return clip_for_embed(formatted)


def spoiler_text(text: str):
    return f"||{text}||"


def get_refs(text: str) -> list[str]:
    # fetch mentions and channels
    mentions = re.findall(DiscordMentions.pattern, text)
    channels = re.findall(DiscordChannels.pattern, text)
    return channels + mentions


def rm_refs(text: str) -> tuple[str, list[str]]:
    refs = get_refs(text)
    text = DiscordMentions.process(text)
    text = DiscordChannels.process(text)
    return text, refs


def format_reply_embed(message: Message) -> Embed:
    # TODO: not finalized.
    content = message.content
    if not content or len(content) > 100:
        content = content[:100] + "..."

    jump = message.jump_url  # direct link to the message

    embed = Embed(
        description=f"{content}\n\n[Link]({jump})",
        timestamp=(
            message.created_at if isinstance(message.created_at, datetime) else None
        ),
    )

    _ = embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.display_avatar.url,
    )

    return embed
