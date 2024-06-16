from database.models import Subject
from dto.subject import BaseSubjectModel, AddSubjectModel
from repositories.base import BaseRepository


class SubjectService:
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    @staticmethod
    async def model_dump(model: Subject) -> BaseSubjectModel:
        return BaseSubjectModel.model_validate(model, from_attributes=True)

    async def dump_subjects(self, subjects: list[Subject]) -> list[BaseSubjectModel]:
        return [await self.model_dump(subject) for subject in subjects]

    async def get_subject(self, subject_id: int, dump: bool = False) -> Subject | BaseSubjectModel:
        subject = await self.repository.get_one(subject_id)
        return await self.model_dump(subject) if dump else subject

    async def get_all_subjects(self) -> list[Subject]:
        subjects = await self.repository.get_all()
        return await self.dump_subjects(subjects)

    async def add_subject(self, form: AddSubjectModel):
        await self.repository.add_item(form.model_dump())
