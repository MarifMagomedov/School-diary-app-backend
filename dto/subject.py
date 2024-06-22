from pydantic import BaseModel, UUID4

from dto.marks import BaseMarkModel


class BaseSubjectModel(BaseModel):
    id: int
    subject_name: str


class AddSubjectModel(BaseModel):
    subject_name: str


class SubjectInScheduleModel(BaseSubjectModel):
    marks: list[BaseMarkModel]
