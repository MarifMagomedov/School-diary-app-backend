from fastapi import APIRouter

from database.methods import Database
from database.models import Subject
from json_data.subjects import json_subjects_names
from json_data.teachers import json_teachers

router = APIRouter(
    prefix="/subjects",
)


@router.get("/{subject_name}/teachers")
async def get_subject_teachers(subject_name: str):
    teachers = await Database.get_subject_teachers(subject_name)
    return json_teachers(teachers)


@router.get('/all')
async def get_subject_all():
    subjects = await Database.get_all_subjects()
    return json_subjects_names(subjects)
