import asyncio
from random import choice

from database.connection import session_factory
from database.connection import engine
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
]

sch_id = uuid4()
school = School(id=sch_id)
role_teacher = Role(id=1, name='teacher')
role_student = Role(id=2, name='student')
role_manager = Role(id=3, name='manager')
manager = Manager(
    id=uuid4(),
    school=school.id,
    name=choice(names),
    surname=choice(surnames),
    middle_name=choice(middle_names),
    age=choice(range(1, 100)),
    role=3,
    register_code=uuid4()
)


async def init_school_and_roles():
    async with session_factory() as session:
        session.add(school)
        await session.commit()
        session.add(role_student)
        session.add(role_teacher)
        session.add(role_manager)
        await session.commit()
        session.add(manager)
        await session.commit()


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


def init_subjects():
    subjects = []
    for subject in subjects_names:
        subject = Subject(
            subject_name=subject,
            school=sch_id
        )
        subjects.append(subject)
    return subjects


def init_students(subjects: list[Subject]):
    students = []
    teachers = []

    while len(students) <= 60:
        user_id = uuid4()
        name = choice(names)
        surname = choice(surnames)
        middle_name = choice(middle_names)
        student = Student(
            id=user_id,
            name=name,
            surname=surname,
            middle_name=middle_name,
            age=choice(range(16, 20)),
            role=2,
            school=sch_id,
            register_code=uuid4()
        )
        students.append(student)

    for subject in subjects:
        user_id = uuid4()
        name = choice(names)
        surname = choice(surnames)
        middle_name = choice(middle_names)
        teacher = Teacher(
            id=user_id,
            name=name,
            surname=surname,
            middle_name=middle_name,
            age=choice(range(30, 70)),
            role=1,
            school=sch_id,
            register_code=uuid4()
        )
        teacher.subjects.append(subject)
        teachers.append(teacher)
    return students, teachers


async def init_classes():
    global school
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_school_and_roles()

    async with session_factory() as session:
        subjects = init_subjects()
        students, teachers = init_students(subjects)
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
        for number, word, teacher in zip(number, words, teachers):
            s = [students.pop() for i in range(10)]
            _class = Class(
                id=uuid4(),
                class_number=number,
                class_word=word,
                classroom_teacher=teacher,
                school=sch_id
            )
            for i in s:
                _class.students.append(i)
                i.student_class = _class
            classes.append(_class)
        session.add_all(classes)
        await session.commit()


asyncio.run(init_classes())
