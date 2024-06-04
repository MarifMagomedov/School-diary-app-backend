from uuid import uuid4, UUID
from pydantic import Field

from .cls import BaseClassModel
from .person import Person


class BaseTeacherModel(Person):
    teacher_class: BaseClassModel | None = None


class NewTeacherModel(BaseTeacherModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    subjects: int
    teacher_class: UUID | None = None


type TeacherDTO = NewTeacherModel | BaseTeacherModel
