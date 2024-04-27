from pydantic import UUID4
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

from .models import Base, Student, Teacher, Subject, Class
from .connection import session_factory, engine


class Database:
    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def check_exist_user(user_type: str, user_id: UUID4) -> Student | Teacher:
        async with session_factory() as session:
            if user_type == 'student':
                return await session.get(Student, user_id)
            elif user_type == 'teachers':
                return await session.get(Teacher, user_id)

    @staticmethod
    async def register_student(**form):
        async with session_factory() as session:
            student = Student(**form)
            session.add(student)
            await session.commit()

    @staticmethod
    async def register_teacher(**form):
        async with session_factory() as session:
            teacher = Teacher(**form)
            session.add(teacher)
            await session.commit()

    @staticmethod
    async def get_all_table_items(table) -> list[Teacher | Subject | Class | Student]:
        async with session_factory() as session:
            query = select(table)
            items = await session.execute(query)
            return items.scalars().all()

    @staticmethod
    async def get_all_subjects() -> list[Subject]:
        async with session_factory() as session:
            query = select(Subject).distinct(Subject.subject_name)
            items = await session.execute(query)
            return items.scalars().all()

    @staticmethod
    async def get_subject_teachers(subject_name: str) -> list[Teacher]:
        async with session_factory() as session:
            query = select(Teacher).join(Subject).where(
                Subject.subject_name == subject_name
            )
            teachers = await session.execute(query)
            return teachers.unique().scalars().all()

    @staticmethod
    async def get_class(class_id: UUID4):
        async with session_factory() as session:
            cls = await session.get(Class, class_id)
            return cls

    @staticmethod
    async def delete_teacher(teacher_id: UUID4):
        async with session_factory() as session:
            teacher = await session.get(Teacher, teacher_id)
            teacher.subjects = []
            await session.delete(teacher)
            await session.commit()
            return teacher
