from uuid import UUID
from starlette.exceptions import HTTPException

from database.models import Class
from errors.class_errors import ClassesErrors
from repositories.base import BaseRepository
from dto.cls import ClassDTO


class ClassService:
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    @staticmethod
    async def _check_classes(classes):
        if not classes:
            raise ClassesErrors.classes_not_found_error

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
        await self._check_classes(cls)
        return await self.model_dump(cls, dto_model) if dump else cls

    async def get_all_classes(self, dto_model: ClassDTO):
        classes = await self.repository.get_all()
        await self._check_classes(classes)
        return await self.dump_classes(classes, dto_model)
