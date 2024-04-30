from uuid import UUID
from typing import NewType, Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette import status

from database.dto.teacher import TeacherModel
from database.methods import Database
from teachers.schemas import AddNewTeacherSchema, EditTeacherSchema

router = APIRouter(
    prefix="/teachers",
    tags=["teacher"]
)


@router.delete('/{teacher_id}')
async def delete_teacher(teacher_id: UUID) -> JSONResponse:
    await Database.delete_teacher(teacher_id)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Teacher deleted successfully"
        }
    )


@router.post('/add')
async def add_teacher(form: Annotated[AddNewTeacherSchema, Depends()]) -> JSONResponse:
    await Database.add_teacher(form)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'message': 'Teacher added successfully'}
    )


@router.put('/update', response_model=TeacherModel)
async def update_teacher(form: Annotated[EditTeacherSchema, Depends()]):
    pass
