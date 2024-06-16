from pydantic import UUID4

from database.models import Class
from repositories.base import BaseRepository
from dto.cls import ClassDTO, AddClassModel


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
        class_id: UUID4,
        dto_model: ClassDTO = None,
        dump: bool = False
    ) -> Class | ClassDTO:
        cls = await self.repository.get_one(class_id)
        return await self.model_dump(cls, dto_model) if dump else cls

    async def get_all_classes(self, dto_model: ClassDTO) -> list[ClassDTO]:
        classes = await self.repository.get_all()
        return await self.dump_classes(classes, dto_model)

    async def update_class(self, class_id: UUID4, **update_data) -> None:
        await self.repository.update(class_id, **update_data)

    async def update_class_teacher(self, class_id: UUID4, teacher_id: UUID4):
        await self.repository.update_class_teacher(class_id, teacher_id)

    async def add_class(self, form: AddClassModel):
        await self.repository.add_item(form.model_dump())

