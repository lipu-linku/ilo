from typing import Self

from discord import Bot, ForumChannel, TextChannel, VoiceChannel, Webhook
from discord.errors import Forbidden, NotFound


# singleton
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
        self.cache: dict[int, Webhook] = dict()
        self.__initialized = True

    async def get_webhook(
        self,
        channel: TextChannel | VoiceChannel | ForumChannel,
    ) -> Webhook | None:
        # get from cache
        channel_id = channel.id
        webhook = self.cache.get(channel_id)
        if webhook:
            try:
                await webhook.fetch()
                return webhook
            except NotFound:
                self.cache.pop(channel_id, None)

        # or discord
        try:
            webhooks = await channel.webhooks()
        except Forbidden:
            return None
        for wh in webhooks:
            if wh.user == self.bot.user:
                self.cache[channel_id] = wh
                return wh

        # or make it
        try:
            webhook = await channel.create_webhook(
                name=self.bot.user.name,
                reason="proxy for linku sitelen pona",
            )
            self.cache[channel_id] = webhook
            return webhook
        except Forbidden:
            return None
