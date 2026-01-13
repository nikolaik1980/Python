import requests
import json
from typing import Dict, Any, Optional
from config import Config


class YougileAPI:
    """API клиент для Yougile"""

    def __init__(self):
        self.base_url = Config.BASE_URL
        self.headers = Config.get_auth_headers()

        # Проверяем конфигурацию
        config_errors = Config.validate_config()
        if config_errors:
            raise ValueError(
                "\n".join(config_errors)
            )

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> requests.Response:
        """Базовый метод для выполнения HTTP запросов"""
        url = f"{self.base_url}{endpoint}"

        # Объединяем заголовки
        request_headers = self.headers.copy()
        if 'headers' in kwargs:
            request_headers.update(kwargs['headers'])
            del kwargs['headers']

        # Добавляем логирование для отладки
        print(f"\n[{method}] {url}")
        if 'json' in kwargs:
            json_data = json.dumps(kwargs['json'], ensure_ascii=False)
            print(f"Request body: {json_data}")

        response = requests.request(
            method=method,
            url=url,
            headers=request_headers,
            **kwargs
        )

        print(f"Response status: {response.status_code}")
        if response.text:
            print(f"Response body: {response.text[:500]}")

        return response

    def create_project(
        self,
        project_data: Dict[str, Any]
    ) -> requests.Response:
        """Создание проекта [POST] /api-v2/projects"""
        return self._request("POST", "/projects", json=project_data)

    def update_project(
        self,
        project_id: str,
        project_data: Dict[str, Any]
    ) -> requests.Response:
        """Обновление проекта [PUT] /api-v2/projects/{id}"""
        return self._request(
            "PUT",
            f"/projects/{project_id}",
            json=project_data
        )

    def get_project(self, project_id: str) -> requests.Response:
        """Получение проекта [GET] /api-v2/projects/{id}"""
        return self._request("GET", f"/projects/{project_id}")

    def get_companies(self) -> requests.Response:
        """Получение списка компаний [GET] /api-v2/companies"""
        return self._request("GET", "/companies")

    def validate_auth(self) -> bool:
        """Проверка авторизации через получение списка компаний"""
        response = self.get_companies()
        return response.status_code == 200


class ProjectBuilder:
    """Билдер для создания данных проекта"""

    @staticmethod
    def get_valid_project_data(
        title: str,
        company_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Создание валидных данных проекта"""
        data = {
            "title": title
        }
        if company_id:
            data["companyId"] = company_id
        return data

    @staticmethod
    def get_project_data_with_description(
        title: str,
        description: str,
        company_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Создание данных проекта с описанием"""
        data = {
            "title": title,
            "description": description
        }
        if company_id:
            data["companyId"] = company_id
        return data

    @staticmethod
    def get_invalid_project_data_missing_title(
        company_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Создание невалидных данных проекта (без названия)"""
        data = {}
        if company_id:
            data["companyId"] = company_id
        return data

    @staticmethod
    def get_invalid_project_data_empty_title(
        company_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Создание невалидных данных проекта (пустое название)"""
        data = {"title": ""}
        if company_id:
            data["companyId"] = company_id
        return data

    @staticmethod
    def get_update_data(
        new_title: str,
        new_description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Данные для обновления проекта"""
        data = {"title": new_title}
        if new_description is not None:
            data["description"] = new_description
        return data
