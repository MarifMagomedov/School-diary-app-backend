from starlette.exceptions import HTTPException
from starlette import status


class UserAlreadyRegister(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Вы уже зарегистрированы!'
        )


class InvalidToken(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Войдите в аккаунт!'
        )


class InvalidUserRole(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='У вас нет доступа к данной странице'
        )


class InvalidLoginData(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Проверьте введеные данные!'
        )


class UserAlreadyNotRegister(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Сначала нужно зарегистрировать аккаунт!'
        )
