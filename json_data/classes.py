from database.models import Class


def json_classes(classes: list[Class]) -> list[dict]:
    response_data = []

    for cls in classes:
        response_data.append(json_class(cls))

    return response_data


def json_class(cls: Class) -> dict:

    class_json = {
        'id': cls.id,
        'class_number': cls.class_number,
        'class_word': cls.class_word,
        'classroom_teacher': cls.classroom_teacher.name if cls.classroom_teacher else None,
    }

    return class_json
