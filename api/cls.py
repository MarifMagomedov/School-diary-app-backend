from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette import status
from starlette.responses import JSONResponse

from dto.teacher import BaseTeacherModel
from utils.dependencies import get_class_service, get_teacher_service
from dto.cls import BaseClassModel, ClassModel, AddClassModel
from services import ClassService, TeacherService

router = APIRouter(
    tags=['class'],
    prefix="/class",
)


@router.get('/all')
async def get_all_classes(
    class_service: Annotated[ClassService, Depends(get_class_service)]
) -> list[BaseClassModel]:
    classes = await class_service.get_all_classes(BaseClassModel)
    return classes


@router.get('/{class_id}')
async def get_one_class(
    class_id: UUID4,
    class_service: Annotated[ClassService, Depends(get_class_service)],
) -> ClassModel:
    cls = await class_service.get_class(class_id, ClassModel, dump=True)
    return cls


@router.patch('/{class_id}/teacher/{teacher_id}')
async def update_class_teacher(
    class_id: UUID4,
    teacher_id: UUID4,
    teacher_service: Annotated[TeacherService, Depends(get_teacher_service)],
    class_service: Annotated[ClassService, Depends(get_class_service)]
) -> BaseTeacherModel:
    await class_service.update_class_teacher(class_id, teacher_id)
    teacher = await teacher_service.get_teacher(teacher_id)
    return await teacher_service.model_dump(teacher)


@router.post('/add')
async def add_class(
    form: AddClassModel,
    class_service: Annotated[ClassService, Depends(get_class_service)]
) -> JSONResponse:
    await class_service.add_class(form)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'message': 'Class added successfully'}
    )