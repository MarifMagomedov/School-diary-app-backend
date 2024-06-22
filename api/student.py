from fastapi import APIRouter, Depends
from typing import Annotated

from pydantic import UUID4
from starlette import status
from starlette.responses import JSONResponse

from dto.schedule import ScheduleModel
from dto.student import StudentModel, AddStudentModel, UpdateStudentModel
from services import StudentService, ClassService, ScheduleService
from utils.dependencies import get_student_service, get_class_service, get_schedule_service

router = APIRouter(
    tags=['students'],
    prefix='/students',
)


@router.post('/add')
async def add_student(
    form: AddStudentModel,
    students_service: Annotated[StudentService, Depends(get_student_service)],
    class_service: Annotated[ClassService, Depends(get_class_service)]
) -> JSONResponse:
    cls = await class_service.get_class(form.student_class)
    form.student_class = cls
    await students_service.add_student(form)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'message': 'Student added successfully'}
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
) -> JSONResponse:
    await student_service.delete_student(student_id)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Student deleted successfully"
        }
    )


@router.put('/{student_id}')
async def update_student(
    student_id: UUID4,
    form: UpdateStudentModel,
    student_service: Annotated[StudentService, Depends(get_student_service)],
):
    await student_service.update_student(student_id, form)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Student edit successfully"
        }
    )


@router.get('/{student_id}/schedule')
async def get_student_schedule(
    schedule_service: Annotated[ScheduleService, Depends(get_schedule_service)],
    student_id: UUID4,
) -> list[ScheduleModel]:
    return await schedule_service.get_student_schedule(student_id)
