from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database_services.utils import session_dependence
from src.database_set.models import UsersModel
from .base import BaseService


class UserService(BaseService):
    model = UsersModel

    @session_dependence()
    async def get_all_users(cls, session: AsyncSession) -> list[dict]:

        query = select(UsersModel)
        result = await session.execute(query)

        return list(map(cls.model_to_dict, result.scalars().all()))
