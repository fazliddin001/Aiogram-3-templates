from loguru import logger


class BaseExceptionHandler:
    """
    A class for handling exceptions and logging them using Loguru.

    :param exception: The exception instance to be logged.
    """

    def __init__(self, exception: BaseException | Exception) -> None:
        if not isinstance(exception, BaseException):
            raise TypeError("The exception must be an instance of Exception or its subclasses.")
        self.exception = exception

    async def handle(self, *, stop_program: bool = False) -> None:
        """
        Logs the exception and optionally stops the program.

        :param stop_program: If True, re-raises the exception to stop the program.
        """
        logger.exception("An exception occurred: {exception}", exception=self.exception)

        if stop_program:
            raise self.exception


class KeyboardInterruptHandler(BaseExceptionHandler):
    async def handle(self, *, stop_program: bool = False) -> None:
        await super().handle(stop_program=stop_program)


class ExceptionHandler(BaseExceptionHandler):
    async def handle(self, *, stop_program: bool = False) -> None:
        # await super().handle(stop_program=stop_program)
        print("Keyboard Interrupt")

        if stop_program is True:
            raise self.exception
