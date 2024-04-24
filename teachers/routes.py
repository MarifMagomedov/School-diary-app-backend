from fastapi import APIRouter

from database.methods import Database
from database.models import Teacher


router = APIRouter(
    prefix="/teachers",
)

