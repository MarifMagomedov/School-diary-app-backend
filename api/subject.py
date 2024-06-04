from typing import Annotated

from fastapi import APIRouter, Depends

from utils.dependencies import get_subject_service, get_teacher_service
from dto.subject import BaseSubjectModel
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
