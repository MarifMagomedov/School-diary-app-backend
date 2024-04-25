from uuid import UUID

from fastapi import APIRouter

from database.methods import Database
from database.models import Teacher


router = APIRouter(
    prefix="/teachers",
)


@router.delete('/{teacher_id}')
async def delete_teacher(teacher_id: UUID):
    await Database.delete_item(Teacher, teacher_id)
    return json_delete_teacher()