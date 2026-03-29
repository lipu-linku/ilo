from enum import Enum
from typing import Self

from cachetools import TTLCache
from discord import ApplicationContext, Bot, DMChannel, GroupChannel, Thread, Webhook
from discord.abc import GuildChannel
from discord.errors import Forbidden, NotFound


class WebhookResult(Enum):
    Success = 1
    NotFound = 2
    NoPermission = 3
    DMChannel = 4

    def __bool__(self) -> bool:
        return self is WebhookResult.Success


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

    async def _get_cached_webhook(
        self, channel: GuildChannel
    ) -> tuple[Webhook | None, WebhookResult]:
        # get from cache
        webhook = self.webhook_cache.get(channel.id)
        if webhook:
            try:
                await webhook.fetch()
                return webhook, WebhookResult.Success
            except NotFound:
                self.webhook_cache.pop(channel.id, None)
        return None, WebhookResult.NotFound

    async def _find_webhook(
        self, channel: GuildChannel
    ) -> tuple[Webhook | None, WebhookResult]:
        try:
            webhooks = await channel.webhooks()
        except Forbidden:
            return None, WebhookResult.NoPermission

        for wh in webhooks:
            if wh.user == self.bot.user:
                self.webhook_cache[channel.id] = wh
                return wh, WebhookResult.Success

        return None, WebhookResult.NotFound

    async def _make_webhook(
        self, channel: GuildChannel
    ) -> tuple[Webhook | None, WebhookResult]:
        try:
            webhook = await channel.create_webhook(
                name=self.bot.user.name,
                reason="proxy for linku sitelen pona",
            )
            self.webhook_cache[channel.id] = webhook
            return webhook, WebhookResult.Success
        except Forbidden:
            return None, WebhookResult.NoPermission

    async def get_webhook(
        self, channel: GuildChannel
    ) -> tuple[Webhook | None, WebhookResult]:
        if isinstance(channel, (DMChannel, GroupChannel)):
            return None, WebhookResult.DMChannel
        if isinstance(channel, Thread):
            channel = channel.parent

        wh, res = await self._get_cached_webhook(channel)
        if wh:
            return wh, res

        wh, res = await self._find_webhook(channel)
        if wh:
            return wh, res

        return await self._make_webhook(channel)

    def is_owned_msg(self, message_id: int, user_id: int) -> bool:
        owner_id = self.sender_cache.get(message_id)
        return owner_id == user_id

    async def send(
        self,
        ctx: ApplicationContext,
        channel: GuildChannel,
        *args,
        **kwargs,
    ) -> WebhookResult:
        wh, res = await self.get_webhook(channel)
        if not wh:
            return res

        msg = await wh.send(*args, **kwargs, wait=True)
        self.sender_cache[msg.id] = ctx.author.id
        return WebhookResult.Success
