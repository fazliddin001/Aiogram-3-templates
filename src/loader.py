from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from core.config import bot_config


storage = MemoryStorage()

bot = Bot(
    token=bot_config.token,
    storage=storage,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
    )
)

dp = Dispatcher()
