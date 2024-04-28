from uuid import UUID

from pydantic import BaseModel


class AddNewTeacherSchema(BaseModel):
    name: str
    surname: str
    middle_name: str
    age: int
    email: str | None = None
    vk: str | None = None
    telegram: str | None = None
    subjects: int
    teacher_class: UUID | None = None


class EditTeacherSchema(BaseModel):
    teacher_id: UUID
    name: str
    surname: str
    middle_name: str
    age: str
    subject_name: str
    teacher_class: UUID | None = None
