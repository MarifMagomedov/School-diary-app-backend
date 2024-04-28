from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette import status

from database.methods import Database
from teachers.schemas import AddNewTeacherSchema, EditTeacherSchema

router = APIRouter(
    prefix="/teachers",
)


@router.delete('/{teacher_id}')
async def delete_teacher(teacher_id: UUID):
    await Database.delete_teacher(teacher_id)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Teacher deleted successfully"
        }
    )


@router.post('/add')
async def add_teacher(form: AddNewTeacherSchema):
    await Database.add_teacher(form)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'message': 'Teacher added successfully'}
    )


@router.put('update')
async def update_teacher(form: EditTeacherSchema):
    pass
