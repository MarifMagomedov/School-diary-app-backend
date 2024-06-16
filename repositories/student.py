from pydantic import UUID4
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from dto.student import StudentModel, UpdateStudentModel
from .base import SqlAlchemyRepository
from database.models import Student, Class, Subject
from database.connection import session_factory


class StudentRepository(SqlAlchemyRepository):
    model = Student

    async def get_students_from_class(self, class_id: UUID4):
        async with self.session_factory() as session:
            query = select(Student).where(Student.class_fk == class_id)
            students = await session.execute(query)
            return students.scalars().all()

    async def delete(self, item_id: UUID4) -> None:
        async with session_factory() as session:
            query = select(
                self.model
            ).where(
                self.model.id == item_id
            ).options(
                selectinload(self.model.marks),
                selectinload(self.model.subjects)
            )

            student = await session.execute(query)
            student = student.scalar_one()
            student.subjects = []

            for mark in student.marks:
                await session.delete(mark)

            await session.commit()

            query = delete(self.model).where(self.model.id == item_id)
            await session.execute(query)
            await session.commit()

    async def update_with_cls_and_subjects(self, item_id: UUID4, update_data: UpdateStudentModel) -> None:
        async with self.session_factory() as session:
            student = await session.get(Student, item_id)
            if update_data.student_class:
                cls = await session.get(Class, update_data.student_class)
                student.student_class = cls
            if update_data.subjects:
                for subject_id in update_data.subjects:
                    subject = await session.get(Subject, subject_id)
                    student.subjects.append(subject)
            await session.commit()
