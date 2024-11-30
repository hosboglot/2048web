from typing import List, Any, TypeVar, Generic
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete, func 
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.game.models import Game


class GameDAO(BaseDAO):
    model = Game
    
    @classmethod
    async def find_max_id(cls, session: AsyncSession, filters: BaseModel):
        filter_dict = filters.model_dump(exclude_unset=True)
        logger.info(f"Поиск максимального ID{cls.model.__name__}")
        try:
            query = select(func.max(cls.model.id)).filter_by(**filter_dict)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            return record or 0
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записи с максимальным ID: {e}")
            raise