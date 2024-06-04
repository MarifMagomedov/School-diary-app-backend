from starlette.exceptions import HTTPException


class ClassesErrors:
    @property
    async def classes_not_found_error(self):
        return HTTPException(
            status_code=404,
            detail="classes not found"
        )
