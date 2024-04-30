from .cls import BaseClassModel
from .person import Person


class TeacherModel(Person):
    teacher_class: BaseClassModel | None = None
