from pydantic import UUID4
from sqlalchemy import select

from database.models import Schedule, Student, ScheduleRow
from repositories.base import SqlAlchemyRepository


class ScheduleRepository(SqlAlchemyRepository):
    model = Schedule

    async def get_student_schedule(self, student_id: UUID4) -> Schedule:
        async with self.session_factory() as session:
            query = select(Schedule).where(ScheduleRow.students.any(Student.id == student_id))
            result = await session.execute(query)
            return result.scalars().all()
