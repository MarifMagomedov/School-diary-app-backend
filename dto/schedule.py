import time
from datetime import datetime

from pydantic import BaseModel, field_validator

from dto.subject import BaseSubjectModel, SubjectInScheduleModel


class Homework(BaseModel):
    id: int
    description: str
    additional_files: list | None = None


class ScheduleRowModel(BaseModel):
    # start_date: datetime
    end_date: datetime
    homework: Homework
    subject: SubjectInScheduleModel


class ScheduleModel(BaseModel):
    date: datetime
    rows: list[ScheduleRowModel]


type ScheduleDTO = ScheduleModel | ScheduleRowModel