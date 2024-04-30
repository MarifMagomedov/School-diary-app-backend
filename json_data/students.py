from database.models import Student


def json_student(student: Student) -> dict:
    student_json = {
        'id': student.id,
        'name': student.name,
        'surname': student.surname,
        'middle_name': student.middle_name,
        'age': student.age,
        'email': student.email,
        'vk': student.vk,
        'telegram': student.telegram,
    }
    return student_json


def json_students(students: list[Student]) -> list[dict]:
    response_data = []

    for student in students:
        response_data.append(json_student(student))

    return response_data
