from uuid import uuid4
from pydantic import Field, UUID4, BaseModel

from .cls import BaseClassModel
from .person import Person
from .subject import BaseSubjectModel


class BaseTeacherModel(Person):
    teacher_class: BaseClassModel | None = None
    subjects: list[BaseSubjectModel]


class NewTeacherModel(BaseTeacherModel):
    id: UUID4 = Field(default_factory=lambda: uuid4())
    subjects: int


class UpdateTeacherModel(BaseModel):
    name: str | None = None
    surname: str | None = None
    middle_name: str | None = None
    age: int | None = None
    subjects: list[int] | None = None


type TeacherDTO = NewTeacherModel | BaseTeacherModel
