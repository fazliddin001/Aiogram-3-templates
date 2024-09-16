import logging
from typing import Callable, Sequence, Any
from loguru import logger
from aiogram.types import BotCommand

from src.loader import bot
from src.core.config import bot_config


async def set_bot_commands() -> None:
    """
    This function was created to manage the bot commands

    it gets bot commands from .../src/cor/config.py:bot_config
    and there you can add any commands or remove them

    :return None:
    """
    commands = bot_config.bot_commands

    bot_commands = [
        BotCommand(command=command, description=description) for command, description in commands.items()
    ]

    await bot.set_my_commands(
        bot_commands
    )


class StartUpBot:
    """
    This class should be called in the main function
    and it runs all of the registered functions
    using __call__ dunder method

    >>> startup()
    """
    def __init__(self, *args, **kwargs) -> None:
        # self.functions variable used to save functions which will be called
        # when the __call__ dunder method will be used.
        self.functions: list[Callable] = []

    @logger.catch(TypeError, level=logging.CRITICAL, message="Error has occurred with register function")
    def register(self, functions: Callable | Sequence[Callable] | Any) -> None:
        """
        Register method is used to register function or Sequence of the functions

        the type of Sequence should be list or a tuple

        :param functions:
        :return None:
        """

        if isinstance(functions, (tuple, list)):

            for function in functions:
                if not callable(function):
                    raise TypeError("The function should be callable function which will be used with await")

                self.functions.append(function)

        elif callable(functions):
            self.functions.append(functions)

        else:
            raise TypeError("Invalid valid type entered to the method register")

    @logger.catch(TypeError, level=logging.CRITICAL, message="Error has occurred with call function")
    async def __call__(self, *args, log: bool = True, **kwargs):
        """
        This function calls the registered functions one by one,
        this function should be used before the dispatcher starts
        polling

        :param args:
        :param kwargs:
        :return:
        """

        if log is True:
            logger.log("INFO", bot_config.startup_messages[0])
            print(bot_config.startup_messages[0])

        for function in self.functions:
            await function(*args, **kwargs)

        if log is True:
            logger.log("INFO", bot_config.startup_messages[1])
            print(bot_config.startup_messages[0])


startup = StartUpBot()

startup.register(
    [
        set_bot_commands,
    ]
)
