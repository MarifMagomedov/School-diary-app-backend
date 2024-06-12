from starlette.exceptions import HTTPException


class ClassesNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail='class is not found')
