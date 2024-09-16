from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.row import RowMapping

from sqlalchemy import select

from src.database_set.base import BaseModel
from src.database_services.utils import session_dependence



class BaseService:
    model = BaseModel

    @session_dependence(class_method=True)
    async def get_obj_by_id(cls, obj_id: int, session: AsyncSession) -> dict:
        query = select(cls.model).filter_by(id=obj_id)
        db_response = await session.execute(query)

        if (obj := db_response.scalars().one_or_none()) is None:
            return {}
        else:
            return cls.model_to_dict(obj)

    @staticmethod
    def model_to_dict(model: BaseModel) -> dict:
        return model.as_dict()

    @staticmethod
    def row_to_dict(row: RowMapping) -> dict:
        return dict(row)
