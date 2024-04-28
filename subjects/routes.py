from fastapi import APIRouter

from database.methods import Database
from database.models import Subject
from json_data.subjects import json_subjects
from json_data.teachers import json_teachers

router = APIRouter(
    prefix="/subjects",
)


@router.get("/{subject_id}/teachers")
async def get_subject_teachers(subject_id: int):
    teachers = await Database.get_subject_teachers(subject_id)
    return json_teachers(teachers)


@router.get('/all')
async def get_subject_all():
    subjects = await Database.get_all_table_items(Subject)
    return json_subjects(subjects)
