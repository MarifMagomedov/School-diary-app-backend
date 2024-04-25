from database.models import Teacher


def json_teachers(teachers: list[Teacher]) -> list[dict]:
    response_data = []

    for teacher in teachers:

        teacher_json = {
            'id': teacher.teacher_id,
            'name': teacher.name,
            'surname': teacher.surname,
            'middle_name': teacher.middle_name,
            'email': teacher.email,
            'teacher_class': {
                'class_id': teacher.teacher_class.class_id,
                'class_number': teacher.teacher_class.class_number,
                'class_word': teacher.teacher_class.class_word
            } if teacher.teacher_class else {},
            'subjects': [
                {
                    'subject_id': subject.subject_id,
                    'subject_name': subject.subject_name
                }
                for subject in teacher.subjects
            ]
        }
        response_data.append(teacher_json)

    return response_data
