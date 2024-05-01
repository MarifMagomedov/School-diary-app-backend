from .base import SqlAlchemyRepository
from database.models import Class


class ClassRepository(SqlAlchemyRepository):
    model = Class
