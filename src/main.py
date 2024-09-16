import asyncio
import uvloop
from aiogram.methods import DeleteWebhook

from src.loader import bot, dp
from src.utils.shutdown import shutdown
from src.utils.startup import startup
from src.utils.exceptions import KeyboardInterruptHandler, ExceptionHandler

from src.middlewares.throttling_middleware import ThrottlingMiddleware
from src.handlers import main_router



asyncio.set_event_loop(uvloop.new_event_loop())


throttling_middleware = ThrottlingMiddleware(limit=5)
dp.middleware.setup(throttling_middleware)


async def main():
    await startup()

    try:
        await dp.include_router(main_router)
        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot)
    except KeyboardInterrupt as exc:
        await KeyboardInterruptHandler(exc).handle()
    except Exception as exc:
        await ExceptionHandler(exc).handle()

    await shutdown()


if __name__ == '__main__':
    asyncio.run(main())
