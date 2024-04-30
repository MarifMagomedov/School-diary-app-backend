from uuid import UUID

from fastapi import APIRouter

from database.dto.cls import BaseClassModel, ClassModel
from database.models import Class
from database.methods import Database


router = APIRouter(
    tags=['class'],
    prefix="/classes",
)


@router.get('/all')
async def get_all_classes() -> list[BaseClassModel]:
    classes = await Database.get_all_table_items(Class)
    return [BaseClassModel.model_validate(row, from_attributes=True) for row in classes]


@router.get('/class/{class_id}')
async def get_one_class(class_id: UUID) -> list[ClassModel]:
    cls = await Database.get_class(class_id)
    return [ClassModel.model_validate(row, from_attributes=True) for row in cls]
