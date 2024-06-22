from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import UUID4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Person:
    name: Mapped[str]
    surname: Mapped[str]
    middle_name: Mapped[str]
    age: Mapped[int]
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(nullable=True)
    vk: Mapped[str] = mapped_column(nullable=True)
    telegram: Mapped[str] = mapped_column(nullable=True)
    registered: Mapped[bool] = mapped_column(default=False)
    register_code: Mapped[UUID4] = mapped_column(unique=True, nullable=True)
    role: Mapped[int] = mapped_column(ForeignKey('roles.id'))


class Base(DeclarativeBase):
    pass


class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]


class School(Base):
    __tablename__ = 'schools'

    id: Mapped[UUID4] = mapped_column(primary_key=True)


class Manager(Base, Person):
    __tablename__ = 'managers'

    id: Mapped[UUID4] = mapped_column(primary_key=True)
    school: Mapped[UUID4] = mapped_column(ForeignKey('schools.id'))


class Homework(Base):
    __tablename__ = 'homeworks'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str]

    schedule_row: Mapped['ScheduleRow'] = relationship(
        back_populates='homework',
        uselist=False,
        lazy='selectin'
    )
    schedule_row_fk: Mapped[UUID4] = mapped_column(ForeignKey('schedule_rows.id'))


class ScheduleRow(Base):
    __tablename__ = 'schedule_rows'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    homework: Mapped['Homework'] = relationship(
        back_populates='schedule_row',
        uselist=False,
        lazy='selectin'
    )
    subject: Mapped['Subject'] = relationship(
        back_populates='schedules_rows',
        uselist=False,
        lazy='selectin'
    )
    students: Mapped[list['Student']] = relationship(
        back_populates='schedules_rows',
        uselist=True,
        secondary='schedule_students',
        lazy='selectin'
    )
    schedule: Mapped['Schedule'] = relationship(
        back_populates='rows',
        uselist=False,
        lazy='selectin'
    )
    subject_fk: Mapped[int] = mapped_column(ForeignKey('subjects.id'))
    schedule_fk: Mapped[int] = mapped_column(ForeignKey('schedules.id'))


class Schedule(Base):
    __tablename__ = 'schedules'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(autoincrement=True)

    rows: Mapped[list['ScheduleRow']] = relationship(
        back_populates='schedule',
        uselist=True,
        lazy='selectin'
    )


class Subject(Base):
    __tablename__ = 'subjects'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subject_name: Mapped[str]
    school: Mapped[UUID4] = mapped_column(ForeignKey('schools.id'))

    students: Mapped[list['Student']] = relationship(
        back_populates='subjects',
        secondary='student_subjects',
        uselist=False
    )
    marks: Mapped[list['Mark']] = relationship(
        back_populates='subject',
        uselist=True,
        lazy='selectin'
    )
    teachers: Mapped[list['Teacher']] = relationship(
        back_populates='subjects',
        uselist=True,
        secondary='teacher_subjects',
        lazy='selectin'
    )
    schedules_rows: Mapped[list['ScheduleRow']] = relationship(
        back_populates='subject',
        uselist=True,
        lazy='selectin'
    )
    teacher_fk: Mapped[int] = mapped_column(ForeignKey('teachers.id'), nullable=True)


class Mark(Base):
    __tablename__ = 'marks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mark_value: Mapped[int]
    date: Mapped[datetime]
    subject: Mapped['Subject'] = relationship(back_populates='marks', uselist=False)
    student: Mapped['Student'] = relationship(back_populates='marks', uselist=False)

    subject_fk: Mapped[int] = mapped_column(ForeignKey('subjects.id'))
    student_fk: Mapped[int] = mapped_column(ForeignKey('students.id'))


class Student(Base, Person):
    __tablename__ = 'students'

    id: Mapped[UUID4] = mapped_column(primary_key=True, unique=True)
    private: Mapped[bool] = mapped_column(default=False)
    school: Mapped[UUID4] = mapped_column(ForeignKey('schools.id'))

    subjects: Mapped[list['Subject']] = relationship(
        back_populates='students',
        secondary='student_subjects',
        uselist=True,
        lazy='selectin'
    )
    marks: Mapped[list['Mark']] = relationship(
        back_populates='student',
        uselist=True,
        lazy='selectin'
    )
    student_class: Mapped['Class'] = relationship(
        back_populates='students',
        uselist=False,
    )
    schedules_rows: Mapped[list['ScheduleRow']] = relationship(
        back_populates='students',
        uselist=True,
        secondary='schedule_students',
        lazy='selectin'
    )
    class_fk: Mapped[int] = mapped_column(ForeignKey('classes.id'), nullable=True)


class Class(Base):
    __tablename__ = 'classes'

    id: Mapped[UUID4] = mapped_column(primary_key=True, unique=True)
    class_number: Mapped[int]
    class_word: Mapped[str]
    school: Mapped[UUID4] = mapped_column(ForeignKey('schools.id'))

    classroom_teacher: Mapped['Teacher'] = relationship(
        back_populates='teacher_class',
        lazy='selectin',
    )
    teachers: Mapped[list['Teacher']] = relationship(
        back_populates='classes',
        uselist=True,
        secondary='teacher_classes'
    )
    students: Mapped[list['Student']] = relationship(
        back_populates='student_class',
        uselist=True,
        lazy='subquery',
    )


class Teacher(Base, Person):
    __tablename__ = 'teachers'

    id: Mapped[UUID4] = mapped_column(primary_key=True, unique=True)
    school: Mapped[UUID4] = mapped_column(ForeignKey('schools.id'))

    subjects: Mapped[list['Subject']] = relationship(
        back_populates='teachers',
        secondary='teacher_subjects',
        uselist=True,
        lazy='joined'
    )
    classes: Mapped[list['Class']] = relationship(
        back_populates='teachers',
        uselist=False,
        secondary='teacher_classes',
        lazy='selectin'
    )
    teacher_class: Mapped['Class'] = relationship(
        back_populates='classroom_teacher',
        lazy='selectin'
    )
    class_fk: Mapped[Optional[int]] = mapped_column(ForeignKey('classes.id'), nullable=True)


class TeacherClass(Base):
    __tablename__ = 'teacher_classes'

    teacher_fk = mapped_column(ForeignKey('teachers.id'), primary_key=True)
    class_fk = mapped_column(ForeignKey('classes.id'), primary_key=True)


class TeacherSubject(Base):
    __tablename__ = 'teacher_subjects'

    teacher_fk = mapped_column(ForeignKey('teachers.id'), primary_key=True)
    subject_fk = mapped_column(ForeignKey('subjects.id'), primary_key=True)


class StudentSubject(Base):
    __tablename__ = 'student_subjects'

    student_fk = mapped_column(ForeignKey('students.id'), primary_key=True)
    subject_fk = mapped_column(ForeignKey('subjects.id'), primary_key=True)


class ScheduleStudent(Base):
    __tablename__ = 'schedule_students'

    schedule_fk = mapped_column(ForeignKey('schedule_rows.id'), primary_key=True)
    student_fk = mapped_column(ForeignKey('students.id'), primary_key=True)


type TypeModels = Teacher | Subject | Student | Class | Mark
