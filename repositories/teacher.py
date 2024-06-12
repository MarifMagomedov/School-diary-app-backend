from uuid import uuid4

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .base import SqlAlchemyRepository
from database.models import Teacher, Subject, Class


class TeacherRepository(SqlAlchemyRepository):
    model = Teacher

