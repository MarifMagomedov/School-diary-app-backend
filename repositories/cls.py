from pydantic import UUID4
from sqlalchemy import select

from .base import SqlAlchemyRepository
from database.models import Class, Teacher


class ClassRepository(SqlAlchemyRepository):
    model = Class

    async def update_class_teacher(self, class_id: UUID4, teacher_id: UUID4):
        async with self.session_factory() as session:
            cls = await session.get(self.model, class_id)
            teacher = await session.get(Teacher, teacher_id)
            cls.classroom_teacher = teacher
            await session.commit()
