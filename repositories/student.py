from pydantic import UUID4
from sqlalchemy import select

from .base import SqlAlchemyRepository
from database.models import Student
from database.connection import session_factory


class StudentRepository(SqlAlchemyRepository):
    model = Student

    async def get_students_from_class(self, class_id: UUID4):
        async with self.session_factory() as session:
            query = select(Student).where(Student.class_fk == class_id)
            students = await session.execute(query)
            return students.scalars().all()
