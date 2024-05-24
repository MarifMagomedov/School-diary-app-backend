from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette import status

from dto.teacher import BaseTeacherModel, NewTeacherModel
from services import SubjectService
from services.class_service import ClassService
from services.teacher_service import TeacherService
from utils.dependencies import get_teacher_service, get_class_service, get_subject_service

router = APIRouter(
    prefix="/teachers",
    tags=["teacher"]
)


@router.delete('/{teacher_id}')
async def delete_teacher(
    teacher_id: UUID,
    teacher_service: Annotated[TeacherService, Depends(get_teacher_service)]
) -> JSONResponse:
    await teacher_service.delete_teacher(teacher_id)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Teacher deleted successfully"
        }
    )


@router.post('/add')
async def add_teacher(
    form: NewTeacherModel,
    teacher_service: Annotated[TeacherService, Depends(get_teacher_service)],
    class_service: Annotated[ClassService, Depends(get_class_service)],
    subject_service: Annotated[SubjectService, Depends(get_subject_service)]
) -> JSONResponse:
    if form.teacher_class:
        form.teacher_class = await class_service.get_class(form.teacher_class)
    form.subjects = [await subject_service.get_subject(form.subjects)]
    await teacher_service.add_teacher(form)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'message': 'Teacher added successfully'}
    )


@router.put('/update', response_model=BaseTeacherModel)
async def update_teacher(
    form: Annotated[BaseTeacherModel, Depends()],
    teacher_service: Annotated[TeacherService, Depends(get_teacher_service)],
    class_service: Annotated[ClassService, Depends(get_class_service)]
):
    pass
