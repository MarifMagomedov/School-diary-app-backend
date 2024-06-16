from uuid import uuid4

from pydantic import BaseModel, UUID4, Field

from .person import Person


class BaseClassModel(BaseModel):
    id: UUID4
    class_number: int
    class_word: str


class ClassModel(BaseClassModel):
    classroom_teacher: Person | None = None
    students: list[Person]


class AddClassModel(BaseClassModel):
    id: UUID4 = Field(default_factory=lambda: uuid4())


type ClassDTO = BaseClassModel | ClassModel
