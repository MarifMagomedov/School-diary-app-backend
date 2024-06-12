from abc import ABC, abstractmethod

from pydantic import UUID4
from sqlalchemy import select, update

from database.connection import session_factory
from database.models import TypeModels


class BaseRepository(ABC):
    @abstractmethod
    async def get_one(self, item_id: int | UUID4):
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
    async def delete(self, item_id: int | UUID4):
        raise NotImplementedError

    @abstractmethod
    async def update(self, item_id: int | UUID4, kwargs):
        raise NotImplementedError


class SqlAlchemyRepository(BaseRepository):
    model: TypeModels = None
    session_factory = session_factory

    async def get_one(self, item_id: int | UUID4) -> model:
        async with self.session_factory() as session:
            item = await session.get(self.model, item_id)
            return item

    async def get_all(self):
        async with self.session_factory() as session:
            print(session)
            query = select(self.model)
            print(query)
            items = await session.execute(query)
            return items.unique().scalars().all()

    async def get_by_filter(self):
        pass

    async def add_item(self, form):
        async with self.session_factory() as session:
            item = self.model(**form)
            session.add(item)
            await session.commit()
            return item

    async def delete(self, item_id: int | UUID4) -> None:
        async with self.session_factory() as session:
            deleting_item = await session.get(self.model, item_id)
            await session.delete(deleting_item)
            await session.commit()

    async def update(self, item_id: int, kwargs):
        async with self.session_factory() as session:
            query = update(self.model).where(self.model.id == item_id).values(kwargs)
            print(query)
            await session.execute(query)
            await session.commit()
