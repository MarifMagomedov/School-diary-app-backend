from starlette.exceptions import HTTPException


class ManagerNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail='Менеджер не найден')
