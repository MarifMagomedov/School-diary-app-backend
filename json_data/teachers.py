from database.models import Teacher


def json_teachers(teachers: list[Teacher]) -> list[dict]:
    response_data = []

    for teacher in teachers:

        teacher_json = {
            'id': teacher.id,
            'name': teacher.name,
            'surname': teacher.surname,
            'middle_name': teacher.middle_name,
            'age': teacher.age,
            'email': teacher.email,
            'teacher_class': {
                'id': teacher.teacher_class.id,
                'class_number': teacher.teacher_class.class_number,
                'class_word': teacher.teacher_class.class_word
            } if teacher.teacher_class else {},
            # 'subjects': [
            #     {
            #         'id': subject.id,
            #         'subject_name': subject.subject_name
            #     }
            #     for subject in teacher.subjects
            # ]
        }

        response_data.append(teacher_json)

    return response_data
