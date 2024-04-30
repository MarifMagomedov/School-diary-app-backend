from fastapi import APIRouter

from .utils import register_user
from .schemas import UserRegisterForm


router = APIRouter(
    tags=['auth'],
    prefix="/auth",
)


@router.get("/current_user")
async def get_current_user():
    pass


@router.post("/register")
async def user_register(user_form: UserRegisterForm):
    register_response = await register_user(user_form)
    return register_response


@router.post("/login")
async def user_login():
    pass
