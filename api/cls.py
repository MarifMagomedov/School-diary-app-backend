from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from api.dependencies import get_class_service
from dto.cls import BaseClassModel, ClassModel
from database.models import Class
from services import ClassService

router = APIRouter(
    tags=['class'],
    prefix="/classes",
)


@router.get('/all')
async def get_all_classes(
    class_service: Annotated[ClassService, Depends(get_class_service)]
) -> list[BaseClassModel]:
    classes = await class_service.get_all_classes(BaseClassModel)
    return classes


@router.get('/class/{class_id}')
async def get_one_class(
    class_id: UUID,
    class_service: Annotated[ClassService, Depends(get_class_service)]
) -> list[ClassModel]:
    cls = await class_service.get_class(class_id, ClassModel)
    return cls

