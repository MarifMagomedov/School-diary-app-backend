import asyncio
from random import choice
from uuid import uuid4

from database.connection import session_factory
from database.methods import Database
from database.models import *


names = [
    'Мага', 'Иван', 'Гуль', 'Никита', 'Николай',
    'Бабиджон', 'Сергей', 'Махмуд', 'Ахмед',
    'Андрей', 'Александр', 'Игорь'
]
surnames = [
    'Токийский', 'Иванов', "Евреев", "Жидов",
    "Зэков", "Чуханов", "Какашников", "Заварушкин",
    "Украйнов", "Гитлер", "Ульянов", "Биробиджонво"
]
middle_names = [
    'Магамедович', "Вахабистович", "Адольфович",
    "Геевич", "Сергеевич", "Махмудович",
    "Расулбекович", "Алексеевич", "Максимович"
]
subjects_names = [
    'Обществознание', 'Математика', 'Информатика',
    'История', 'ОБЖ', 'Русский язык', 'Английский язык',
    'Физика', 'Физическая культура', "Программирование",
    'Обществознание', 'Математика', 'История', 'Английский язык'
]


def init_marks():
    marks = []
    while len(marks) < 7000:
        month = choice(range(1, 13))
        day = choice(range(1, 28))
        set_date = datetime(year=2024, month=month, day=day)
        mark = Mark(
            mark_value=choice(range(2, 6)),
            date=set_date
        )
        marks.append(mark)
    return marks


def init_subjects(teachers):
    subjects = []
    for subject, teacher in zip(subjects_names, teachers):
        subject = Subject(
            subject_name=subject,
            teacher=teacher
        )
        subjects.append(subject)
    return subjects


def init_students():
    students = []
    teachers = []

    while len(students) <= 60:
        user_id = uuid4()
        name = choice(names)
        surname = choice(surnames)
        middle_name = choice(middle_names)
        student = Student(
            student_id=user_id,
            name=name,
            surname=surname,
            middle_name=middle_name,
            age=choice(range(16, 20))
        )
        students.append(student)

    while len(teachers) <= len(subjects_names):
        user_id = uuid4()
        name = choice(names)
        surname = choice(surnames)
        middle_name = choice(middle_names)
        teacher = Teacher(
            teacher_id=user_id,
            name=name,
            surname=surname,
            middle_name=middle_name,
            age=choice(range(30, 70))
        )
        teachers.append(teacher)
    return students, teachers


async def init_classes():
    await Database.create_tables()
    students, teachers = init_students()
    subjects = init_subjects(teachers)
    marks = init_marks()

    for i in range(len(students)):
        students[i].subjects = subjects

    m_i = 0
    for student in students:
        for subject in student.subjects:
            marks_count = choice(range(1, 7))
            new_marks = marks[m_i: m_i + marks_count]
            m_i += marks_count
            subject.marks = new_marks
            student.marks.extend(new_marks)

    number = [10, 10, 10, 11, 11, 11]
    words = ['А', "Б", "В", 'А', "Б", "В"]
    classes = []
    async with session_factory() as session:
        for number, word, teacher in zip(number, words, teachers):
            s = [students.pop() for i in range(10)]
            _class = Class(
                class_id=uuid4(),
                class_number=number,
                class_word=word,
                classroom_teacher=teacher,
            )
            for i in s:
                _class.students.append(i)
                i.student_class = _class
            classes.append(_class)
        session.add_all(classes)
        await session.commit()
#
#
# asyncio.run(init_classes())
