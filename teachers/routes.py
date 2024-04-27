from uuid import UUID

from fastapi import APIRouter

from database.methods import Database
from database.models import Teacher
from json_data.subjects import json_subjects_names

router = APIRouter(
    prefix="/teachers",
)


@router.delete('/{teacher_id}')
async def delete_teacher(teacher_id: UUID):
    deleted_teacher = await Database.delete_teacher(teacher_id)
    return json_subjects_names(deleted_teacher.subject)
