from .cls import BaseClassModel
from .person import Person


class BaseTeacherModel(Person):
    teacher_class: BaseClassModel | None = None


class TeacherModel(BaseTeacherModel):
    pass
