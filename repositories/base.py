from abc import ABC, abstractmethod
from uuid import UUID
from sqlalchemy import select

from database.connection import session_factory
from database.models import TypeModels


class BaseRepository(ABC):
    @abstractmethod
    async def get_one(self, item_id: int | UUID):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def get_by_filter(self):
        raise NotImplementedError

    @abstractmethod
    async def add_item(self, form):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, item_id: int | UUID):
        raise NotImplementedError

    @abstractmethod
    async def update(self, item_id: int | UUID):
        raise NotImplementedError


class SqlAlchemyRepository(BaseRepository):
    model: TypeModels = None

    async def get_one(self, item_id: int | UUID) -> model:
        async with session_factory() as session:
            item = await session.get(self.model, item_id)
            return item

    async def get_all(self):
        async with session_factory() as session:
            query = select(self.model)
            items = await session.execute(query)
            return items.unique().scalars().all()

    async def get_by_filter(self):
        pass

    async def add_item(self, form):
        async with session_factory() as session:
            item = self.model(**form)
            session.add(item)
            await session.commit()

    async def delete(self, item_id: int | UUID) -> None:
        async with session_factory() as session:
            deleting_item = await session.get(self.model, item_id)
            print(deleting_item)
            await session.delete(deleting_item)
            await session.commit()

    async def update(self, item_id: int, **kwargs):
        pass
