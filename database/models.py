from datetime import datetime
from typing import Optional, Type
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


class Base(DeclarativeBase):
    pass


class Subject(Base):
    __tablename__ = 'subjects'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subject_name: Mapped[str]

    students: Mapped[list['Student']] = relationship(
        back_populates='subjects',
        secondary='student_subjects',
        uselist=False
    )
    marks: Mapped[list['Mark']] = relationship(
        back_populates='subject',
        uselist=True
    )
    teachers: Mapped[list['Teacher']] = relationship(
        back_populates='subjects',
        uselist=True,
        secondary='teacher_subjects',
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

    subjects: Mapped[list['Subject']] = relationship(
        back_populates='students',
        secondary='student_subjects',
        uselist=True,
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
    class_fk: Mapped[int] = mapped_column(ForeignKey('classes.id'), nullable=True)


class Class(Base):
    __tablename__ = 'classes'

    id: Mapped[UUID4] = mapped_column(primary_key=True, unique=True)
    class_number: Mapped[int]
    class_word: Mapped[str]

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


type TypeModels = Teacher | Subject | Student | Class | Mark
