from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from starlette import status

from dto.auth import RegisterModel, LoginModel
from services import AuthService, TeacherService, StudentService, ManagerService
from utils.dependencies import get_auth_service, get_teacher_service, get_student_service, get_manager_service

router = APIRouter(
    tags=['auth'],
    prefix="/auth",
)


@router.post("/register")
async def register_user(
    form: RegisterModel,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    teacher_service: Annotated[TeacherService, Depends(get_teacher_service)],
    student_service: Annotated[StudentService, Depends(get_student_service)],
    manager_service: Annotated[ManagerService, Depends(get_manager_service)]
):
    if form.role == '1':
        service = teacher_service
    elif form.role == '2':
        service = student_service
    else:
        service = manager_service

    user = await service.check_by_register_code(form.register_code)
    token = await auth_service.register_user(form, user.registered)
    form = form.model_dump()
    form.update({'registered': True})
    await service.update_registered(form, user.id)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'message': 'Вы успешно зарегистрировались', 'token': token}
    )


@router.post("/login")
async def create_access_token(
    form: LoginModel,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    teacher_service: Annotated[TeacherService, Depends(get_teacher_service)],
    student_service: Annotated[StudentService, Depends(get_student_service)],
    manager_service: Annotated[ManagerService, Depends(get_manager_service)]
):
    if form.role == '1':
        user = await teacher_service.get_by_email(form.email)
    elif form.role == '2':
        user = await student_service.get_by_email(form.email)
    else:
        user = await manager_service.get_by_email(form.email)

    token = await auth_service.login_user(form.email, form.password, user.hashed_password, user.registered)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Вы успешно вошли', 'token': token}
    )

# @router.post("/auth/check")
# async def check_user_is_authorized(
#     auth_service: Annotated[AuthService, Depends(get_auth_service)],
#     request: Request
# ):
#     await auth_service.verify_token(request.headers.get('Authorization'))
#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content={'message': 'Пользователь уже авторизован'}
#     )


