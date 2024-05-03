from pydantic import BaseModel
from dto.person import Person


class StudentModel(Person):
    pass


type StudentDTO = StudentModel
