from uuid import UUID

from fastapi import APIRouter

from database.dto.cls import BaseClassModel
from database.models import Class
from database.methods import Database
from json_data.classes import json_classes, json_class

router = APIRouter(
    tags=['class'],
    prefix="/classes",
)


@router.get('/all')
async def get_all_classes() -> list[BaseClassModel]:
    classes = await Database.get_all_table_items(Class)
    return [BaseClassModel.model_validate(row, from_attributes=True) for row in classes]


@router.get('/class/{class_id}')
async def get_one_class(class_id: UUID):
    cls = await Database.get_class(class_id)
    return
