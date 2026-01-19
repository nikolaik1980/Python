import sys
import os

# Добавляем текущую директорию в sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.exc import SQLAlchemyError  # noqa: E402

# Абсолютный импорт (будет работать при запуске из родительской директории)
try:
    from models import Base, Student
    from config import DATABASE_URL
except ImportError:
    # Альтернативный вариант импорта
    from .models import Base, Student
    from .config import DATABASE_URL


@pytest.fixture(scope='session')
def engine():
    """Создание движка базы данных"""
    engine = create_engine(DATABASE_URL, echo=False)
    return engine


@pytest.fixture(scope='session')
def tables(engine):
    """Создание таблиц (если их нет)"""
    try:
        Base.metadata.create_all(engine)
        yield
    except SQLAlchemyError as e:
        print(f"Ошибка при создании таблиц: {e}")
        raise


@pytest.fixture
def db_session(engine, tables):
    """Сессия базы данных для каждого теста"""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def cleanup_test_data(db_session):
    """Фикстура для очистки тестовых данных"""
    yield

    # Удаляем всех студентов, созданных в тестах
    # с user_id в определенном диапазоне для безопасности
    try:
        db_session.query(Student).filter(
            Student.user_id.between(90000, 99999)
        ).delete(synchronize_session=False)
        db_session.commit()
    except Exception as e:
        print(f"Ошибка при очистке данных: {e}")
        db_session.rollback()
