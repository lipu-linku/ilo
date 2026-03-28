from typing import Self

from cachetools import TTLCache
from discord import (
    ApplicationContext,
    Bot,
    ForumChannel,
    TextChannel,
    VoiceChannel,
    Webhook,
)
from discord.errors import Forbidden, NotFound


class WebhookManager:
    __initialized: bool = False
    __instance: Self | None = None

    def __new__(cls, bot: Bot) -> Self:
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, bot: Bot):
        if self.__initialized:
            return
        self.bot: Bot = bot
        self.webhook_cache: dict[int, Webhook] = dict()
        self.sender_cache: TTLCache[int, int] = TTLCache(maxsize=99999, ttl=1800)
        # TODO: will these ever be args?
        self.__initialized = True

    async def get_webhook(
        self,
        channel: TextChannel | VoiceChannel | ForumChannel,
    ) -> Webhook | None:
        # get from cache
        channel_id = channel.id
        webhook = self.webhook_cache.get(channel_id)
        if webhook:
            try:
                await webhook.fetch()
                return webhook
            except NotFound:
                self.webhook_cache.pop(channel_id, None)

        # or discord
        try:
            webhooks = await channel.webhooks()
        except Forbidden:
            return None
        for wh in webhooks:
            if wh.user == self.bot.user:
                self.webhook_cache[channel_id] = wh
                return wh

        # or make it
        try:
            webhook = await channel.create_webhook(
                name=self.bot.user.name,
                reason="proxy for linku sitelen pona",
            )
            self.webhook_cache[channel_id] = webhook
            return webhook
        except Forbidden:
            return None

    def is_owned_msg(self, message_id: int, user_id: int) -> bool:
        owner_id = self.sender_cache.get(message_id)
        return owner_id == user_id

    async def send(
        self,
        ctx: ApplicationContext,
        channel: TextChannel | VoiceChannel | ForumChannel,
        *args,
        **kwargs,
    ) -> bool:
        webhook = await self.get_webhook(channel)
        if not webhook:
            return False

        msg = await webhook.send(*args, **kwargs, wait=True)
        self.sender_cache[msg.id] = ctx.author.id
        return True
