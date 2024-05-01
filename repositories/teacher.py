from uuid import uuid4

from database.connection import session_factory
from dto.teacher import BaseTeacherModel
from .base import SqlAlchemyRepository
from database.models import Teacher, Subject, Class


class TeacherRepository(SqlAlchemyRepository):
    model = Teacher
