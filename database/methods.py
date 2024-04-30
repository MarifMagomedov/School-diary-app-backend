from typing import Type
from uuid import uuid4

from pydantic import UUID4
from sqlalchemy import select

from teachers.schemas import AddNewTeacherSchema
from .models import Base, Student, Teacher, Subject, Class
from .connection import session_factory, engine


class Database:
    @classmethod
    async def create_tables(cls):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @classmethod
    async def check_exist_user(cls, user_type: str, user_id: UUID4) -> Student | Teacher:
        async with session_factory() as session:
            if user_type == 'student':
                return await session.get(Student, user_id)
            elif user_type == 'teachers':
                return await session.get(Teacher, user_id)

    @classmethod
    async def register_student(cls, **form):
        async with session_factory() as session:
            student = Student(**form)
            session.add(student)
            await session.commit()

    @classmethod
    async def register_teacher(cls, **form):
        async with session_factory() as session:
            teacher = Teacher(**form)
            session.add(teacher)
            await session.commit()

    @classmethod
    async def get_all_table_items(
        cls,
        table: Type[Teacher | Subject | Class | Student]
    ) -> list[Teacher | Subject | Class | Student]:
        async with session_factory() as session:
            query = select(table)
            items = await session.execute(query)
            return items.unique().scalars().all()

    @classmethod
    async def get_subject_teachers(cls, subject_id: int) -> list[Teacher]:
        async with session_factory() as session:
            subject = await session.get(Subject, subject_id)
            return subject.teachers

    @classmethod
    async def get_one_table_item(
        cls,
        table: Type[Teacher | Subject | Class | Student], item_id: int | UUID4
    ) -> Type[Teacher | Subject | Class | Student]:
        async with session_factory() as session:
            item = await session.get(table, item_id)
            return item

    @classmethod
    async def delete_teacher(cls, teacher_id: UUID4):
        async with session_factory() as session:
            teacher = await session.get(Teacher, teacher_id)
            await session.delete(teacher)
            await session.commit()

    @classmethod
    async def add_teacher(cls, form: AddNewTeacherSchema):
        async with session_factory() as session:
            subject = await session.get(Subject, form.subjects)
            form.subjects = [subject]
            if form.teacher_class:
                teacher_class = await cls.get_one_table_item(Class, form.teacher_class)
                form.teacher_class = teacher_class
            teacher = Teacher(
                id=uuid4(),
                **form.model_dump()
            )
            session.add(teacher)
            await session.commit()
