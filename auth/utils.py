from starlette import status
from fastapi.responses import JSONResponse

from .schemas import UserRegisterForm
from database.methods import Database


async def register_user(user_form: UserRegisterForm) -> JSONResponse:
    user_exist = await Database.check_exist_user(user_form.user_type, user_form.user_id)
    print(user_exist)
    if user_exist and user_exist.id != user_form.user_id:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Invalid user id for register user"}
        )
    if user_exist.registered:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": "User already registered"}
        )
    await Database.register_student(**user_form.model_dump())
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'message': 'Account created successfully'}
    )
