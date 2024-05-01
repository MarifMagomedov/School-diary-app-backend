import services
import repositories


async def get_class_service():
    return services.ClassService(repositories.ClassRepository())


async def get_teacher_service():
    return services.TeacherService(repositories.TeacherRepository())


async def get_subject_service():
    return services.SubjectService(repositories.SubjectRepository())
