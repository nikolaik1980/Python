import pytest
import uuid
import time
from api.yougile_api import YougileAPI


class TestSimpleProjects:

    @pytest.fixture(autouse=True)
    def setup(self):
        try:
            self.api = YougileAPI()
        except ValueError as e:
            pytest.skip(f"Конфигурация не настроена: {e}")

    def generate_project_name(self):
        """Генерация уникального имени проекта"""
        return f"Test Project {uuid.uuid4().hex[:8]}"

    # TEST 1: Create project (POSITIVE)
    def test_1_create_project(self):
        """Тест создания проекта"""
        project_name = self.generate_project_name()

        # Создаем проект
        response = self.api.create_project({"title": project_name})
        assert response.status_code in [200, 201], (
            f"Create failed: {response.text}"
        )

        project_id = response.json()["id"]
        print(f"✓ Project created with ID: {project_id}")

        # Проверяем через GET
        get_response = self.api.get_project(project_id)
        assert get_response.status_code == 200, (
            f"Get failed: {get_response.text}"
        )

        project_data = get_response.json()
        assert project_data["title"] == project_name, (
            f"Title mismatch: {project_data}"
        )

        return project_id

    # TEST 2: Get project (POSITIVE)
    def test_2_get_project(self):
        """Тест получения проекта"""
        # Сначала создаем проект
        project_name = self.generate_project_name()
        create_response = self.api.create_project({"title": project_name})
        assert create_response.status_code in [200, 201]

        project_id = create_response.json()["id"]

        # Получаем проект
        response = self.api.get_project(project_id)
        assert response.status_code == 200, (
            f"Get failed: {response.text}"
        )

        project_data = response.json()
        assert project_data["id"] == project_id
        assert project_data["title"] == project_name

        print(f"✓ Project retrieved: {project_data['title']}")

    # TEST 3: Update project (POSITIVE)
    def test_3_update_project(self):
        """Тест обновления проекта"""
        # Создаем проект
        project_name = self.generate_project_name()
        create_response = self.api.create_project({"title": project_name})
        assert create_response.status_code in [200, 201]

        project_id = create_response.json()["id"]

        # Обновляем проект
        new_name = f"Updated {uuid.uuid4().hex[:8]}"
        update_response = self.api.update_project(
            project_id, {"title": new_name}
        )
        assert update_response.status_code == 200, (
            f"Update failed: {update_response.text}"
        )

        # Проверяем обновление
        time.sleep(0.5)
        get_response = self.api.get_project(project_id)
        project_data = get_response.json()

        assert project_data["title"] == new_name, (
            f"Update not applied: {project_data}"
        )

        print(f"✓ Project updated from '{project_name}' to '{new_name}'")

    # TEST 4: Create without title (NEGATIVE)
    def test_4_create_without_title(self):
        """Тест создания проекта без названия"""
        response = self.api.create_project({})
        assert response.status_code in [400, 422], (
            f"Expected error, got {response.status_code}"
        )
        print(
            f"✓ Correctly rejected project without title: {response.text}"
        )

    # TEST 5: Get invalid ID (NEGATIVE)
    def test_5_get_invalid_id(self):
        """Тест получения несуществующего проекта"""
        response = self.api.get_project("invalid_id_123")
        assert response.status_code in [404, 400], (
            f"Expected error, got {response.status_code}"
        )
        print(
            f"✓ Correctly rejected invalid project ID: {response.text}"
        )

    # TEST 6: Update invalid ID (NEGATIVE)
    def test_6_update_invalid_id(self):
        """Тест обновления несуществующего проекта"""
        response = self.api.update_project(
            "invalid_id_123", {"title": "New Name"}
        )
        assert response.status_code in [404, 400], (
            f"Expected error, got {response.status_code}"
        )
        print(
            "✓ Correctly rejected update for invalid project ID: "
            f"{response.text}"
        )
