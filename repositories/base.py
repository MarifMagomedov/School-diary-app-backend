from abc import ABC, abstractmethod


class BaseRepository(ABC):
    def __init__(self, model):
        self.model = model

    @abstractmethod
    async def get_one(self):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_by_filter(self):
        pass

    @abstractmethod
    async def delete(self):
        pass

    @abstractmethod
    async def update(self):
        pass
