import atexit
import logging
from typing import Callable, Sequence, Any
from loguru import logger
from src.core.config import bot_config


class Shutdown:
    def __init__(self, *args, **kwargs) -> None:
        self.functions: list[Callable[..., Any]] = []

    @logger.catch(TypeError, level=logging.CRITICAL, message="Error has occurred with register function")
    def register(self, functions: Callable[..., Any] | Sequence[Callable[..., Any]]) -> None:
        """
        Registers a function or a sequence of functions to be called at shutdown.

        :param functions: A callable or a sequence of callables (list or tuple).
        :raises TypeError: If any item is not callable.
        """
        if isinstance(functions, (tuple, list)):
            for function in functions:
                if not callable(function):
                    raise TypeError("Each item must be callable.")
                self.functions.append(function)
        elif callable(functions):
            self.functions.append(functions)
        else:
            raise TypeError("Invalid type provided. Must be callable or a sequence of callables.")


    @staticmethod
    @logger.catch(TypeError, level=logging.CRITICAL, message="Error has occurred with register_at_exit function")
    def register_at_exit(function: Callable) -> None:
        """
        Registers a function to be called upon program exit using `atexit`.

        :param function: A function to be registered for program exit.
        """
        atexit.register(function)

    @logger.catch(TypeError, level=logging.CRITICAL, message="Error has occurred with call function")
    async def __call__(self, *args, log: bool = True, **kwargs) -> None:
        """
        Calls all registered functions in sequence. Logs messages before and after execution.

        :param args: Positional arguments to pass to each function.
        :param kwargs: Keyword arguments to pass to each function.
        :param log: Whether to log shutdown messages.
        """
        if log:
            logger.info("INFO", bot_config.shutdown_messages[0])
            print(bot_config.startup_messages[0])

        for function in self.functions:
            await function(*args, **kwargs)

        if log:
            logger.info("INFO", bot_config.shutdown_messages[1])
            print(bot_config.startup_messages[0])


shutdown = Shutdown()
