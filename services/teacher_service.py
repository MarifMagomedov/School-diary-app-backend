from uuid import UUID, uuid4

from database.models import Teacher
from dto.teacher import BaseTeacherModel, NewTeacherModel
from errors.teacher_errors import TeacherErrors
from repositories.base import BaseRepository


class TeacherService:
    def __init__(self, teacher_repository: BaseRepository):
        self.repository = teacher_repository

    @staticmethod
    async def _check_teachers(teachers: list[Teacher]) -> None:
        if not teachers:
            raise TeacherErrors.teacher_not_found_error

    @staticmethod
    async def model_dump(model: Teacher) -> BaseTeacherModel:
        return BaseTeacherModel.model_validate(model, from_attributes=True)

    async def dump_teachers(self, teachers: list[Teacher]) -> list[BaseTeacherModel]:
        return [await self.model_dump(teacher) for teacher in teachers]

    async def get_all_teachers(self) -> list[Teacher | BaseTeacherModel]:
        teachers = await self.repository.get_all()
        await self._check_teachers(teachers)
        return await self.dump_teachers(teachers)

    async def delete_teacher(self, teacher_id: UUID):
        return await self.repository.delete(teacher_id)

    async def add_teacher(self, form: NewTeacherModel):
        await self.repository.add_item(form.model_dump())
