from database.models import Class


def json_classes(classes: list[Class]) -> list[dict]:
    response_data = []

    for cls in classes:
        class_json = {
            'class_id': cls.class_id,
            'class_number': cls.class_number,
            'class_word': cls.class_word,
            'classroom_teacher': cls.classroom_teacher.name,
        }
        response_data.append(class_json)

    return response_data


def json_class(cls: Class) -> dict:

    class_json = {
        'class_id': cls.class_id,
        'class_number': cls.class_number,
        'class_word': cls.class_word,
        'classroom_teacher': cls.classroom_teacher.name,
    }

    return class_json
