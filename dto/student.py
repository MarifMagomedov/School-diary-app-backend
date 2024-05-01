from pydantic import BaseModel

from database.models import Person


class Student(Person, BaseModel):
    pass