from database.models import Subject


def json_subjects_names(subjects: list[Subject]) -> list[dict]:
    response_data = []

    for subject in subjects:
        subject_json = {
            'subject_name': subject.subject_name,
        }
        response_data.append(subject_json)

    return response_data
