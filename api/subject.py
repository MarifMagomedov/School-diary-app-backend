from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from utils.dependencies import get_subject_service, get_teacher_service
from dto.subject import BaseSubjectModel, AddSubjectModel
from dto.teacher import BaseTeacherModel
from services import TeacherService
from services.subject_service import SubjectService

router = APIRouter(
    tags=['subject'], prefix="/subjects",
)


@router.get('/all')
async def get_subject_all(
    subject_service: Annotated[SubjectService, Depends(get_subject_service)]
) -> list[BaseSubjectModel]:
    subjects = await subject_service.get_all_subjects()
    return subjects


@router.post('/add')
async def add_subject(
    form: AddSubjectModel,
    subject_service: Annotated[SubjectService, Depends(get_subject_service)]
):
    await subject_service.add_subject(form)
    from starlette import status
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'message': 'Subject added successfully'}
    )