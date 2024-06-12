from starlette.exceptions import HTTPException


class SubjectsErrors:
    @property
    async def subjects_not_found_error(self):
        return HTTPException(
            status_code=404,
            detail="subjects not found"
        )
