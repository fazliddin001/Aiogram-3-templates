from datetime import datetime, timezone
from typing import Any

from sqlalchemy import inspect, Integer, DateTime, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from functools import lru_cache
from .db_config import metadata


# Here is the BaseModel which you can use
# Notice, you can create your models without registering metadata and
# id, it will run perfectly

class BaseModel(DeclarativeBase):
    __abstract__ = True
    metadata = metadata

    id: Mapped[int] = mapped_column(Integer, primary_key=True, auto_increment=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=text("TIMEZONE('UTC', NOW())"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=text("TIMEZONE('UTC', NOW())"),
        onupdate=datetime.now(timezone.utc),
    )

    @classmethod
    @lru_cache(maxsize=None)
    def column_names(cls) -> list[str]:
        """
        Returns a list of column names.
        :return:
        """

        mapper = inspect(cls)
        return [column.name for column in mapper.columns]

    def get_columns(self) -> list[Any]:
        """
        Retrieves the values of columns from the model instance based on column names.

        :return: List of column values.
        """
        column_values = []
        for column_name in self.column_names():
            try:
                column_value = getattr(self, column_name)
                column_values.append(column_value)
            except AttributeError:
                pass

        return column_values

    def as_dict(self) -> dict[str, Any]:
        """
        Returns a dictionary representation of the model instance.
        :return:
        """
        columns_dict: dict[str, Any] = {}

        for column_name in self.column_names():
            try:
                columns_dict[column_name] = getattr(self, column_name)
            except AttributeError:
                pass

        return columns_dict
