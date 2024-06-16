from starlette.exceptions import HTTPException
from starlette import status


class TeacherNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail='Учитель не найден')
