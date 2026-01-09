"""Скрипт для проверки авторизации в Yougile API"""
import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from api.yougile_api import YougileAPI


def main():
    """Основная функция"""
    print("Проверка авторизации Yougile API")
    print("=" * 40)

    # Проверяем конфигурацию
    errors = Config.validate_config()
    if errors:
        print("Ошибки конфигурации:")
        for error in errors:
            print(f"  - {error}")
        print("\nУбедитесь, что файл .env существует и содержит:")
        print("  YOUGILE_API_TOKEN=ваш_токен")
        return 1

    print(f"Base URL: {Config.BASE_URL}")
    print(f"API Token configured: {bool(Config.API_TOKEN)}")
    print(f"Username configured: {bool(Config.API_USERNAME)}")

    try:
        # Создаем клиент API
        api = YougileAPI()
        print("\nПроверка соединения с API...")

        # Создаем тестовый проект
        import uuid
        test_project_name = f"Test Project {uuid.uuid4().hex[:8]}"
        project_data = {"title": test_project_name}

        print(f"Создаем тестовый проект: {test_project_name}")
        response = api.create_project(project_data)

        if response.status_code in [200, 201]:
            project_info = response.json()
            print("✓ Авторизация успешна!")
            print("✓ Проект создан:")
            print(f"  ID: {project_info.get('id')}")
            print(f"  Название: {project_info.get('title')}")
            company_id = project_info.get('companyId', 'Не указан')
            print(f"  Company ID: {company_id}")

            # Пробуем получить созданный проект
            project_id = project_info.get('id')
            get_response = api.get_project(project_id)
            if get_response.status_code == 200:
                print("✓ Проект успешно получен по ID")
            else:
                status_code = get_response.status_code
                print(f"⚠ Не удалось получить проект: {status_code}")

            return 0
        else:
            status_code = response.status_code
            print(f"✗ Ошибка создания проекта: {status_code}")
            print(f"✗ Ответ сервера: {response.text}")
            return 1

    except Exception as e:
        print(f"✗ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
