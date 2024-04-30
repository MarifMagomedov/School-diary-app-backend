from database.models import Teacher


def json_teacher(teacher: Teacher):
    teacher_json = {
        'id': teacher.id,
        'name': teacher.name,
        'surname': teacher.surname,
        'middle_name': teacher.middle_name,
        'age': teacher.age,
        'email': teacher.email,
        'vk': teacher.vk,
        'telegram': teacher.telegram,
        'teacher_class': {
            'id': teacher.teacher_class.id,
            'class_number': teacher.teacher_class.class_number,
            'class_word': teacher.teacher_class.class_word
        } if teacher.teacher_class else {}
    }
    return teacher_json


def json_teachers(teachers: list[Teacher]) -> list[dict]:
    response_data = []

    for teacher in teachers:
        response_data.append(json_teacher(teacher))

    return response_data
