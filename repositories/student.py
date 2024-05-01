from .base import SqlAlchemyRepository
from database.models import Student


class StudentRepository(SqlAlchemyRepository):
    model = Student
