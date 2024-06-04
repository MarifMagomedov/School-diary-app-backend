from uuid import UUID

from pydantic import BaseModel

from database.models import Class
from repositories.base import BaseRepository
from dto.cls import ClassDTO


class ClassService:
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    @staticmethod
    async def model_dump(db_model: Class, dto_model: ClassDTO) -> ClassDTO:
        return dto_model.model_validate(db_model, from_attributes=True)

    async def dump_classes(self, classes: list[Class], dto_model: ClassDTO) -> list[ClassDTO]:
        return [await self.model_dump(cls, dto_model) for cls in classes]

    async def get_class(
        self,
        class_id: UUID,
        dto_model: ClassDTO = None,
        dump: bool = False
    ) -> Class | ClassDTO:
        cls = await self.repository.get_one(class_id)
        return await self.model_dump(cls, dto_model) if dump else cls

    async def get_all_classes(self, dto_model: ClassDTO) -> list[ClassDTO]:
        classes = await self.repository.get_all()
        return await self.dump_classes(classes, dto_model)
