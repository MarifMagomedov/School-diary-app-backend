import time
from datetime import datetime

from pydantic import BaseModel, field_validator

from dto.subject import BaseSubjectModel, SubjectInScheduleModel


class Homework(BaseModel):
    description: str


class ScheduleRowModel(BaseModel):
    homework: Homework
    subject: SubjectInScheduleModel


class ScheduleModel(BaseModel):
    date: datetime
    rows: list[ScheduleRowModel]
