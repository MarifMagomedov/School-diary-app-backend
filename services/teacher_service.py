from pydantic import UUID4

from database.models import Teacher
from dto.auth import RegisterModel
from dto.teacher import BaseTeacherModel, NewTeacherModel, UpdateTeacherModel
from repositories.base import BaseRepository
import utils.errors.teacher_errors as errors


class TeacherService:
    def __init__(self, teacher_repository: BaseRepository):
        self.repository = teacher_repository

    @staticmethod
    async def model_dump(model: Teacher) -> BaseTeacherModel:
        return BaseTeacherModel.model_validate(model, from_attributes=True)

    async def dump_teachers(self, teachers: list[Teacher]) -> list[BaseTeacherModel]:
        return [await self.model_dump(teacher) for teacher in teachers]

    async def get_all_teachers(self) -> list[Teacher]:
        teachers = await self.repository.get_all()
        return await self.dump_teachers(teachers)

    async def delete_teacher(self, teacher_id: UUID4):
        return await self.repository.delete(teacher_id)

    async def add_teacher(self, form: NewTeacherModel) -> Teacher:
        await self.repository.add_item(form.model_dump())

    async def get_free_teachers(self) -> list[BaseTeacherModel]:
        teachers = await self.repository.get_all()
        return list(filter(lambda x: x.teacher_class is None, teachers))

    async def get_teacher(self, teacher_id: UUID4, dump: bool = False) -> Teacher | BaseTeacherModel:
        teacher = await self.repository.get_one(teacher_id)
        return self.model_dump(teacher) if dump else teacher

    async def update_teacher(self, teacher_id: UUID4, update_data: UpdateTeacherModel):
        await self.repository.update(teacher_id, update_data)

    async def check_by_register_code(self, register_code: str) -> Teacher:
        teacher = await self.repository.get_by_attribute(self.repository.model.register_code, register_code)
        if not teacher:
            return errors.TeacherNotFoundError()
        return teacher

    async def update_registered(self, form: dict, teacher_id: UUID4) -> None:
        await self.repository.update(teacher_id, form)

    async def get_by_email(self, email: str) -> Teacher:
        return await self.repository.get_by_attribute(self.repository.model.email, email)
