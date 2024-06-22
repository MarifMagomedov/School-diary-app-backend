from pydantic import BaseModel


class BaseMarkModel(BaseModel):
    id: int
    mark_value: int
