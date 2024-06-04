from pydantic import BaseModel, UUID4


class Person(BaseModel):
    id: UUID4
    name: str
    surname: str
    middle_name: str
    age: int
    email: str | None = None
    vk: str | None = None
    telegram: str | None = None
