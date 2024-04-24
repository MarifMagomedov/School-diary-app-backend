from datetime import datetime
from typing import Optional

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

    subject_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subject_name: Mapped[str]

    students: Mapped[list['Student']] = relationship(
        back_populates='subjects', secondary='student_subjects',
        uselist=False, cascade='all,delete'
    )
    marks: Mapped[list['Mark']] = relationship(
        back_populates='subject', uselist=True, cascade='all,delete'
    )
    teacher: Mapped['Teacher'] = relationship(
        back_populates='subjects', uselist=False, cascade='all,delete'
    )
    teacher_fk: Mapped[int] = mapped_column(ForeignKey('teachers.teacher_id'))


class Mark(Base):
    __tablename__ = 'marks'

    mark_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mark_value: Mapped[int]
    date: Mapped[datetime]
    subject: Mapped['Subject'] = relationship(back_populates='marks', uselist=False)
    student: Mapped['Student'] = relationship(back_populates='marks', uselist=False)

    subject_fk: Mapped[int] = mapped_column(ForeignKey('subjects.subject_id'))
    student_fk: Mapped[int] = mapped_column(ForeignKey('students.student_id'))


class Student(Base, Person):
    __tablename__ = 'students'

    student_id: Mapped[UUID4] = mapped_column(primary_key=True, unique=True)
    private: Mapped[bool] = mapped_column(default=False)

    subjects: Mapped[list['Subject']] = relationship(
        back_populates='students', secondary='student_subjects',
        uselist=True
    )
    marks: Mapped[list['Mark']] = relationship(
        back_populates='student', uselist=True, cascade='all,delete'
    )
    student_class: Mapped['Class'] = relationship(
        back_populates='students', uselist=False, cascade='all,delete'
    )
    class_fk: Mapped[int] = mapped_column(ForeignKey('classes.class_id'))


class Class(Base):
    __tablename__ = 'classes'

    class_id: Mapped[UUID4] = mapped_column(primary_key=True, unique=True)
    class_number: Mapped[int]
    class_word: Mapped[str]

    classroom_teacher: Mapped['Teacher'] = relationship(back_populates='teacher_class', lazy='subquery')
    teachers: Mapped[list['Teacher']] = relationship(
        back_populates='classes', uselist=True,
        secondary='teacher_classes', cascade='all,delete'
    )
    students: Mapped[list['Student']] = relationship(
        back_populates='student_class', uselist=True, cascade='all,delete'
    )


class Teacher(Base, Person):
    __tablename__ = 'teachers'

    teacher_id: Mapped[UUID4] = mapped_column(primary_key=True, unique=True)

    subjects: Mapped[list['Subject']] = relationship(back_populates='teacher', uselist=True, lazy='joined')
    classes: Mapped[list['Class']] = relationship(
        back_populates='teachers', uselist=False,
        secondary='teacher_classes', cascade='all,delete'
    )
    teacher_class: Mapped['Class'] = relationship(
        back_populates='classroom_teacher',
        cascade='all,delete', lazy='subquery'
    )
    class_fk: Mapped[Optional[int]] = mapped_column(ForeignKey('classes.class_id'))


class TeacherClass(Base):
    __tablename__ = 'teacher_classes'

    teacher_fk = mapped_column(ForeignKey('teachers.teacher_id'), primary_key=True)
    class_fk = mapped_column(ForeignKey('classes.class_id'), primary_key=True)


class TeacherSubject(Base):
    __tablename__ = 'teacher_subjects'

    teacher_fk = mapped_column(ForeignKey('teachers.teacher_id'), primary_key=True)
    subject_fk = mapped_column(ForeignKey('subjects.subject_id'), primary_key=True)


class StudentSubject(Base):
    __tablename__ = 'student_subjects'

    student_fk = mapped_column(ForeignKey('students.student_id'), primary_key=True)
    subject_fk = mapped_column(ForeignKey('subjects.subject_id'), primary_key=True)

