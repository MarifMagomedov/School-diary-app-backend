from fastapi import APIRouter

from database.dto.subject import BaseSubjectModel
from database.dto.teacher import BaseTeacherModel
from database.methods import Database
from database.models import Subject


router = APIRouter(
    tags=['subject'], prefix="/subjects",
)


@router.get("/{subject_id}/teachers")
async def get_subject_teachers(subject_id: int) -> list[BaseTeacherModel]:
    teachers = await Database.get_subject_teachers(subject_id)
    return [BaseTeacherModel.model_validate(row, from_attributes=True) for row in teachers]


@router.get('/all')
async def get_subject_all() -> list[BaseSubjectModel]:
    subjects = await Database.get_all_table_items(Subject)
    return [BaseSubjectModel.model_validate(row, from_attributes=True) for row in subjects]
