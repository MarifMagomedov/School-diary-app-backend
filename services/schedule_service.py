from datetime import datetime, timedelta

from fastapi import UploadFile
from pydantic import UUID4

from database.models import Schedule
from dto.schedule import ScheduleModel, ScheduleRowModel, ScheduleDTO
from repositories.base import BaseRepository


class ScheduleService:
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    @staticmethod
    async def model_dump(db_model: Schedule, dto_model: ScheduleDTO = ScheduleModel) -> ScheduleRowModel:
        return dto_model.model_validate(db_model, from_attributes=True)

    @staticmethod
    async def get_date(year: int, week: int) -> list[datetime]:
        start_day = datetime.strptime(f'{year}-{week}-1', "%Y-%W-%w").date()
        end_day = start_day + timedelta(days=5)
        return start_day, end_day

    async def dump_schedules(
        self,
        schedules: list[Schedule],
        dto_model: ScheduleDTO = ScheduleModel
    ) -> list[ScheduleDTO]:
        return [await self.model_dump(schedules, dto_model) for schedules in schedules]

    async def get_student_schedule(
        self,
        student_id:
        UUID4,
        year: int,
        week: int,
    ) -> list[ScheduleDTO]:
        dates = await self.get_date(year, week)

        schedules = await self.repository.get_student_schedule(student_id, *dates)
        dumped_schedules = await self.dump_schedules(schedules)

        return dumped_schedules

    async def get_student_schedule_rows(self, student_id, year, week):
        dates = await self.get_date(year, week)

        schedules = await self.repository.get_student_schedule(student_id, *dates)
        schedule_rows = [row for schedule in schedules for row in schedule.rows]
        schedule_rows.sort(key=lambda x: x.subject.subject_name)

        dumped_schedule_rows = await self.dump_schedules(schedule_rows, ScheduleRowModel)

        return dumped_schedule_rows

# async def upload_homework_files(self, homework_id: int, files: list[UploadFile]):
#     files = [str(await file.read()) for file in files]
#     await self.repository.update(homework_id, {'files': files})
