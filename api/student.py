from fastapi import APIRouter, Depends
from typing import Annotated

from pydantic import UUID4
from starlette.responses import JSONResponse

from dto.student import StudentModel
from services import StudentService
from utils.dependencies import get_student_service

router = APIRouter(
    tags=['students'],
    prefix='/students',
)


@router.get('/{class_id}')
async def get_class_students(
    class_id: UUID4,
    students_service: Annotated[StudentService, Depends(get_student_service)]
) -> list[StudentModel]:
    students = await students_service.get_students_from_class(class_id)
    return students


@router.delete('/{student_id}')
async def delete_student(
    student_id: UUID4,
    student_service: Annotated[StudentService, Depends(get_student_service)]
) -> StudentModel:
    await student_service.delete_student(student_id)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Student deleted successfully"
        }
    )
