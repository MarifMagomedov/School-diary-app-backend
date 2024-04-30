from fastapi import APIRouter

from database.dto.subject import BaseSubjectModel
from database.dto.teacher import TeacherModel
from database.methods import Database
from database.models import Subject


router = APIRouter(
    tags=['subject'], prefix="/subjects",
)


@router.get("/{subject_id}/teachers")
async def get_subject_teachers(subject_id: int) -> list[TeacherModel]:
    teachers = await Database.get_subject_teachers(subject_id)
    return [TeacherModel.model_validate(row, from_attributes=True) for row in teachers]


@router.get('/all')
async def get_subject_all() -> list[BaseSubjectModel]:
    subjects = await Database.get_all_table_items(Subject)
    return [BaseSubjectModel.model_validate(row, from_attributes=True) for row in subjects]
