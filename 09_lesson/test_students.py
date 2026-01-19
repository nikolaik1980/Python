"""
Тесты для работы со студентами в базе данных.
Включают тесты на добавление, изменение и soft delete.
"""
import sys
import os

# Добавляем текущую директорию в sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


import pytest  # noqa: E402
from sqlalchemy.exc import IntegrityError  # noqa: E402

try:
    from models import Student
except ImportError:
    from .models import Student


class TestStudentCRUD:
    """Тесты CRUD операций для студентов"""

    def test_add_student(self, db_session, cleanup_test_data):
        """
        Тест добавления нового студента.
        """
        # Подготовка тестовых данных
        test_student = Student(
            user_id=90001,
            level="Intermediate",
            education_form="group",
            subject_id=1,
            is_deleted=False
        )

        # Добавление студента
        db_session.add(test_student)
        db_session.commit()

        # Получение студента из базы
        retrieved_student = db_session.query(Student).filter_by(
            user_id=90001
        ).first()

        # Проверки
        assert retrieved_student is not None
        assert retrieved_student.user_id == 90001
        assert retrieved_student.level == "Intermediate"
        assert retrieved_student.education_form == "group"
        assert retrieved_student.subject_id == 1
        assert retrieved_student.is_deleted is False

        print(f"Студент {retrieved_student.user_id} успешно добавлен")

    def test_update_student(self, db_session, cleanup_test_data):
        """
        Тест обновления данных студента.
        """
        # Сначала создаем студента
        test_student = Student(
            user_id=90002,
            level="Beginner",
            education_form="personal",
            subject_id=2,
            is_deleted=False
        )

        db_session.add(test_student)
        db_session.commit()

        # Обновляем данные студента
        student_to_update = db_session.query(Student).filter_by(
            user_id=90002
        ).first()

        student_to_update.level = "Pre-Intermediate"
        student_to_update.education_form = "group"
        student_to_update.subject_id = 3

        db_session.commit()

        # Проверяем обновленные данные
        updated_student = db_session.query(Student).filter_by(
            user_id=90002
        ).first()

        assert updated_student.level == "Pre-Intermediate"
        assert updated_student.education_form == "group"
        assert updated_student.subject_id == 3

        print(f"Данные студента {updated_student.user_id} успешно обновлены")

    def test_soft_delete_student(self, db_session, cleanup_test_data):
        """
        Тест мягкого удаления студента.
        """
        # Создаем студента для удаления
        test_student = Student(
            user_id=90003,
            level="Advanced",
            education_form="group",
            subject_id=1,
            is_deleted=False
        )

        db_session.add(test_student)
        db_session.commit()

        # Выполняем мягкое удаление
        student_to_delete = db_session.query(Student).filter_by(
            user_id=90003
        ).first()

        student_to_delete.is_deleted = True
        db_session.commit()

        # Проверяем, что студент помечен как удаленный
        deleted_student = db_session.query(Student).filter_by(
            user_id=90003
        ).first()

        assert deleted_student.is_deleted is True

        # Проверяем, что мы можем найти удаленного студента
        all_students = db_session.query(Student).filter_by(
            user_id=90003
        ).all()

        assert len(all_students) == 1

        print(f"Студент {deleted_student.user_id} помечен как удаленный")

    def test_unique_user_id_constraint(self, db_session, cleanup_test_data):
        """
        Тест проверки уникальности user_id.
        """
        # Создаем первого студента
        student1 = Student(
            user_id=90004,
            level="Beginner",
            education_form="group",
            subject_id=1
        )

        db_session.add(student1)
        db_session.commit()

        # Пытаемся создать второго студента с таким же user_id
        student2 = Student(
            user_id=90004,
            level="Intermediate",
            education_form="personal",
            subject_id=2
        )

        db_session.add(student2)

        # Ожидаем ошибку IntegrityError
        with pytest.raises(IntegrityError):
            db_session.commit()

        # Откатываем сессию после ошибки
        db_session.rollback()

        print("Уникальность user_id успешно проверена")


def test_retrieve_all_active_students(db_session, cleanup_test_data):
    """
    Тест получения только активных (не удаленных) студентов.
    """
    # Создаем несколько студентов
    students_data = [
        (90005, "Beginner", "group", 1, False),
        (90006, "Intermediate", "personal", 2, False),
        (90007, "Advanced", "group", 3, True),
    ]

    for user_id, level, form, subject_id, is_deleted in students_data:
        student = Student(
            user_id=user_id,
            level=level,
            education_form=form,
            subject_id=subject_id,
            is_deleted=is_deleted
        )
        db_session.add(student)

    db_session.commit()

    # Получаем только активных студентов
    active_students = db_session.query(Student).filter_by(
        is_deleted=False
    ).all()

    # Должно быть 2 активных студента
    assert len(active_students) == 2

    # Проверяем, что у всех активных студентов is_deleted = False
    for student in active_students:
        assert student.is_deleted is False
        assert student.user_id in [90005, 90006]

    print(f"Найдено {len(active_students)} активных студентов")
