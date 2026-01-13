import pytest
import uuid


@pytest.fixture
def unique_project_name():
    """Генерация уникального имени проекта"""
    return f"Test Project {uuid.uuid4().hex[:8]}"


@pytest.fixture
def unique_updated_project_name():
    """Генерация уникального имени для обновления"""
    return f"Updated Project {uuid.uuid4().hex[:8]}"


@pytest.fixture
def cleanup_project_ids():
    """Фикстура для хранения ID проектов"""
    project_ids = []
    yield project_ids
    # В Yougile API обычно нет метода удаления проектов,
    # поэтому просто выводим информацию о созданных проектах
    if project_ids:
        print(f"\nСоздано тестовых проектов: {len(project_ids)}")
        for pid in project_ids:
            print(f"  - {pid}")
