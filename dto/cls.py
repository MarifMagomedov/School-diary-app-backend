from uuid import UUID

from pydantic import BaseModel

from .person import Person


class BaseClassModel(BaseModel):
    id: UUID
    class_number: int
    class_word: str


class ClassModel(BaseClassModel):
    classroom_teacher: Person
    students: list[Person]


type ClassDTO = BaseClassModel | ClassModel
