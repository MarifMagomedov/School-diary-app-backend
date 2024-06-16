from fastapi.exceptions import HTTPException


class StudentNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail='Ученик не найден')