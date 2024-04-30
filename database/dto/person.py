from uuid import UUID

from pydantic import BaseModel


class Person(BaseModel):
    id: UUID
    name: str
    surname: str
    middle_name: str
    age: int
    email: str | None = None
    vk: str | None = None
    telegram: str | None = None
