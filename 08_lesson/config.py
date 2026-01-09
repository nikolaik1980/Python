import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Конфигурация тестов"""
    BASE_URL = "https://ru.yougile.com/api-v2"
    API_TOKEN = os.getenv("YOUGILE_API_TOKEN")
    API_USERNAME = os.getenv("YOUGILE_API_USERNAME", "")
    API_PASSWORD = os.getenv("YOUGILE_API_PASSWORD", "")

    # Тестовые данные
    TEST_COMPANY_ID = os.getenv("TEST_COMPANY_ID", "")

    @classmethod
    def get_auth_headers(cls):
        """Получение заголовков авторизации"""
        headers = {"Content-Type": "application/json"}

        if cls.API_TOKEN:
            headers["Authorization"] = f"Bearer {cls.API_TOKEN}"
        elif cls.API_USERNAME and cls.API_PASSWORD:
            import base64
            creds = f"{cls.API_USERNAME}:{cls.API_PASSWORD}"
            encoded = base64.b64encode(creds.encode()).decode()
            headers["Authorization"] = f"Basic {encoded}"

        return headers

    @classmethod
    def validate_config(cls):
        """Проверка конфигурации"""
        errors = []

        if not cls.API_TOKEN and (
            not cls.API_USERNAME or not cls.API_PASSWORD
        ):
            msg = (
                "Не указаны данные для авторизации. Установите "
                "YOUGILE_API_TOKEN или "
                "YOUGILE_API_USERNAME/YOUGILE_API_PASSWORD"
            )
            errors.append(msg)

        return errors
