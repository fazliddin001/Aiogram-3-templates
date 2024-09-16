from pathlib import Path

from pydantic_settings import BaseSettings
from loguru import logger


# Declaring BASE_DIR variable which saves the path:
# /home/.../src/  or for windows  c:/.../src/
BASE_DIR = Path(__file__).resolve().parent.parent


# Settings class reads all variables from
# src/.env file
class Settings(BaseSettings):
    """
    Declare .env file on the src file:
    ``src/.env``
    """
    # bot configuration

    BOT_TOKEN: str
    BOT_NAME: str | None = None
    BOT_USERNAME: str | None = None

    # database configuration
    # by default it uses postgresql

    DB_USERNAME: str | None = None
    DB_PASSWORD: str | None = None
    DB_HOST: str | None = None
    DB_PORT: str | None = None
    DB_NAME: str | None = None

    # logging configurations
    LOG_LEVEL: str | None = 'INFO'

    class Config:
        env_file = BASE_DIR / ".env"


# declaring settings variable
settings = Settings()


# DatabaseConfig class users settings variable
# which was declared before and users
# part of the database which is concentrated
# to database, and provides structured
# usage, also it uses slots which good for memory
class DatabaseConfig:
    """
    This class used for saving configurations of the database
    """
    settings: Settings = settings
    __slots__ = ("username", "password", "host", "port", "db_name", "auto_commit",
                 "auto_rollback")

    def __init__(self):
        self.username: str = self.settings.DB_USERNAME or ""
        self.password: str = self.settings.DB_PASSWORD or ""
        self.host: str = self.settings.DB_HOST or ""
        self.port: str = self.settings.DB_PORT or ""
        self.db_name: str = self.settings.DB_NAME or ""
        # auto commit variable is used in src/database_services/utils to define
        # if the decorator commits after successfully got result
        self.auto_commit: bool = True
        # auto rollback variable is used to the similar thing
        # it's the definition if the decorator got an error
        self.auto_rollback: bool = True


    @property
    def async_db_url(self) -> str:
        """
        The method was created to define the url with
        driver for postgresql database
        which is called asyncpg(Async library used as driver by sqlalchemy)
        :return str:
        """
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"

    @property
    def sync_db_url(self) -> str:
        """
        The method was created to define the url with
        driver for postgresql database
        which is called psycopg2(Sync library used as driver by sqlalchemy)

        the primary use case is in alembic/env.py \n
        >>> # config.set_main_option("sqlalchemy.url", database_config.sync_db_url)

        :return str:
        """
        return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"


# BotConfig class was created to handle bot infos as
# DatabaseConfig does with database infos
class BotConfig:
    """
    This class was created to define the configuration of
    bot.
    """
    settings: Settings = settings

    __slots__ = ("token", "username", "name", "bot_commands", "startup_messages", "shutdown_messages")

    def __init__(self):
        self.token: str = self.settings.BOT_TOKEN
        self.name: str = self.settings.BOT_NAME
        self.username: str = self.settings.BOT_USERNAME
        self.bot_commands: dict[str, str] = {
            "start": "Starting/Restarting the bot",
        }
        # two strings which will be called when bot starting
        self.startup_messages: list[str] = [
            "Bot is starting.",
            "Bot is running."
        ]
        # two strings which will be called when bot shutting down
        self.shutdown_messages: list[str] = [
            "Bot is shutting down.",
            "Bot was turned off."
        ]

# declaring bot_config variable and database_config variable which
# will be used in the other modules later

bot_config = BotConfig()

database_config = DatabaseConfig()

# Define the log file path and create files if it's important
LOG_FILE = BASE_DIR / "logs" / "logs.log"

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

LOG_LEVEL = settings.LOG_LEVEL or "INFO"

FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"

# Configure the logger
logger.remove()  # Remove the default logger

logger.add(
    LOG_FILE,
    format=FORMAT,
    level=LOG_LEVEL,
    rotation="1 week",
    retention="1 month",
    enqueue=True,
    compression="zip"
)
