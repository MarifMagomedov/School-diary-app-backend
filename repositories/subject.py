from sqlalchemy import select

from database.connection import session_factory
from .base import SqlAlchemyRepository
from database.models import Subject


class SubjectRepository(SqlAlchemyRepository):
    model = Subject
