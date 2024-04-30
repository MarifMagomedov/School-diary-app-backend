from pydantic import BaseModel


class BaseSubjectModel(BaseModel):
    id: int
    subject_name: str
