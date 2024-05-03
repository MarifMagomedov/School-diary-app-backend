from uuid import UUID

from database.models import Student
from repositories.base import BaseRepository
from dto.student import StudentDTO


class StudentService:
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    @staticmethod
    async def model_dump(db_model: Student, dto_model: StudentDTO) -> StudentDTO:
        return dto_model.model_validate(db_model, from_attributes=True)

    async def dump_students(self, students: list[Student], dto_model: StudentDTO) -> list[StudentDTO]:
        return [await self.model_dump(student, dto_model) for student in students]

    async def get_student(
        self,
        student_id: UUID,
        dto_model: StudentDTO = None,
        dump: bool = False
    ) -> Student | StudentDTO:
        student = await self.repository.get_one(student_id)
        return await self.model_dump(student, dto_model) if dump else student

    async def get_all_students(self, dto_model: StudentDTO):
        students = await self.repository.get_all()
        return await self.dump_students(students, dto_model)
