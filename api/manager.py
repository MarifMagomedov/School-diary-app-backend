from typing import Annotated

from fastapi import APIRouter, Depends


router = APIRouter(
    prefix="/managers",
    tags=["managers"]
)
