from pydantic import BaseModel, UUID4


class BaseSubjectModel(BaseModel):
    id: int
    subject_name: str


class AddSubjectModel(BaseModel):
    subject_name: str