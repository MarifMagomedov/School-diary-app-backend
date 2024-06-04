from starlette.exceptions import HTTPException


class TeacherErrors:
    @property
    async def teacher_not_found_error(self):
        return HTTPException(
            status_code=404,
            detail="teachers not found"
        )
