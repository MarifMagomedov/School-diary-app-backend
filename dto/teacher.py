from uuid import uuid4
from pydantic import Field, UUID4

from .cls import BaseClassModel
from .person import Person
from .subject import BaseSubjectModel


class BaseTeacherModel(Person):
    teacher_class: BaseClassModel | None = None
    subjects: list[BaseSubjectModel]


class NewTeacherModel(BaseTeacherModel):
    id: UUID4 = Field(default_factory=lambda: uuid4())
    subjects: int


type TeacherDTO = NewTeacherModel | BaseTeacherModel
