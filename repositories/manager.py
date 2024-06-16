from database.models import Manager
from repositories.base import SqlAlchemyRepository


class ManagerRepository(SqlAlchemyRepository):
    model = Manager
