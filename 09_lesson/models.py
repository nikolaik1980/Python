from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base  # Изменено здесь!
from sqlalchemy.sql import expression

Base = declarative_base()  # Теперь импорт из sqlalchemy.orm


class Student(Base):
    """Модель студента с поддержкой soft delete"""
    __tablename__ = 'students'

    user_id = Column(Integer, primary_key=True)
    level = Column(String(50), nullable=False)
    education_form = Column(String(50), nullable=False)
    subject_id = Column(Integer, nullable=False)
    is_deleted = Column(
        Boolean,
        default=False,
        server_default=expression.false(),
        nullable=False
    )

    def __repr__(self):
        return f"<Student(user_id={self.user_id}, level={self.level})>"
