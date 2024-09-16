from __future__ import annotations
from typing import *
from aiogram import BaseMiddleware
from aiogram.types import Message
import time
from collections import defaultdict


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: float = 0.5, key_prefix: str = 'antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        self.throttle_manager = ThrottleManager(limit)
        super(ThrottlingMiddleware, self).__init__()

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        try:
            await self.on_process_event(event, data)
        except CancelHandler:
            # Cancel current handler
            return

        result = await handler(event, data)
        return result

    async def on_process_event(
            self,
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        key = f"{self.prefix}_message_{event.from_user.id}_{event.chat.id}"

        try:
            await self.throttle_manager.throttle(key)
        except Throttled as t:
            await self.event_throttled(event, t)
            raise CancelHandler()

    async def event_throttled(self, event: Message, throttled: Throttled):
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count <= 2:
            await event.answer(f'Too many events.\nTry again in {delta:.2f} seconds.')


class ThrottleManager:
    def __init__(self, rate: float):
        self.rate = rate
        self.bucket = defaultdict(dict)  # Dictionary to store throttling information

    async def throttle(self, key: str):
        now = time.time()
        data = self.bucket.get(key, {"LAST_CALL": now, "EXCEEDED_COUNT": 0})

        called = data["LAST_CALL"]
        delta = now - called
        result = delta >= self.rate or delta <= 0

        data["LAST_CALL"] = now
        data["DELTA"] = delta

        if not result:
            data["EXCEEDED_COUNT"] += 1
        else:
            data["EXCEEDED_COUNT"] = 1

        self.bucket[key] = data

        if not result:
            raise Throttled(key=key, **data)

        return result


class Throttled(Exception):
    def __init__(self, **kwargs):
        self.key = kwargs.pop("key", '<None>')
        self.called_at = kwargs.pop("LAST_CALL", time.time())
        self.rate = kwargs.pop("RATE_LIMIT", None)
        self.exceeded_count = kwargs.pop("EXCEEDED_COUNT", 0)
        self.delta = kwargs.pop("DELTA", 0)
        self.user = kwargs.pop('user', None)
        self.chat = kwargs.pop('chat', None)

    def __str__(self):
        return f"Rate limit exceeded! (Limit: {self.rate} s, " \
               f"exceeded: {self.exceeded_count}, " \
               f"time delta: {round(self.delta, 3)} s)"


class CancelHandler(Exception):
    pass
