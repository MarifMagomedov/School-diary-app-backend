from uuid import uuid4

from pydantic import BaseModel, UUID4, Field
from dto.person import Person


class StudentModel(Person):
    pass


class AddStudentModel(StudentModel):
    id: UUID4 = Field(default_factory=lambda: uuid4())
    student_class: UUID4


class UpdateStudentModel(BaseModel):
    name: str | None = None
    surname: str | None = None
    middle_name: str | None = None
    age: int | None = None
    student_class: UUID4 | None = None
    subjects: list[int] | None = None


type StudentDTO = StudentModel
