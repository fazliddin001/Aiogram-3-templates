from functools import wraps
from typing import Callable

from loguru import logger
from src.database_set.db_config import session_factory
from src.core.config import database_config


def no_op_decorator(func):
    return func


def session_dependence(
        auto_commit: bool = database_config.auto_commit,
        auto_rollback: bool = database_config.auto_rollback,
        log_on_error: bool = True,
        class_method: bool = True
    ) -> Callable:

    """
    This decorator was created to manage exceptions on the well-structured
    database which is based on class methods.

    The functions using this decorator has to have the parameter: session
    which will entered as a session

    :param auto_commit: commits the code if the parameter is given as True otherwise
    the stmt should be commited manually.
    the default argument of auto_rollback can be changed by changing src/core/config:database_config.auto_commit
    :param auto_rollback: calls the rollback method of the session if there is an error,
    the default argument of auto_rollback can be changed by changing src/core/config:database_config.auto_rollback
    :param log_on_error: This parameter logs an error if the error occurs, but not prints it.
    :param class_method: if this parameter set True the functions which users this decorator
    become class method
    :return:
    """

    def decorator(func: Callable) -> Callable:

        # Choose the appropriate decorator based on `class_method`
        _d = classmethod if class_method else no_op_decorator

        @_d
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with session_factory() as _session:
                try:
                    # Call the decorated function and pass the session
                    response = await func(*args, **kwargs, session=_session)

                    # Commit if auto_commit is True
                    if auto_commit:
                        await _session.commit()

                    return response  # Return response after commit

                except Exception as exc:
                    # Log the error if log_on_error is True
                    if log_on_error:
                        logger.error(f"Error occurred in {func.__name__}: {exc}")

                    # Rollback if auto_rollback is True
                    if auto_rollback:
                        await _session.rollback()

                    raise exc  # Re-raise the caught exception to propagate it

        return wrapper

    return decorator
