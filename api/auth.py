from fastapi import APIRouter


router = APIRouter(
    tags=['auth'],
    prefix="/auth",
)


@router.get("/current_user")
async def get_current_user():
    pass


@router.post("/register")
async def user_register(user_form):
    pass


@router.post("/login")
async def user_login():
    pass
