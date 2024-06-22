from pydantic import UUID4

from database.models import Schedule
from dto.schedule import ScheduleModel, ScheduleRowModel
from repositories.base import BaseRepository


class ScheduleService:
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    @staticmethod
    async def model_dump(db_model: Schedule) -> ScheduleRowModel:
        return ScheduleModel.model_validate(db_model, from_attributes=True)

    async def dump_schedules(self, schedules: list[Schedule]) -> list[ScheduleModel]:
        return [await self.model_dump(schedules) for schedules in schedules]

    async def get_student_schedule(self, student_id: UUID4) -> list[ScheduleModel]:
        schedules = await self.repository.get_student_schedule(student_id)
        # for schedule in schedules:
        #     for row in schedule.rows:
        #         try:
        #             print(schedule.date,  row.subject.marks[0].date)
        #         except IndexError:
        #             pass
        #         row.subject.marks = list(filter(lambda mark: mark.date == schedule.date, row.subject.marks))
        dumped_schedules = await self.dump_schedules(schedules)
        return dumped_schedules
