from config import Config


def test_config_loaded():
    """Тест проверки загрузки конфигурации"""
    # Проверяем, что .env файл загружен
    assert Config.BASE_URL == "https://ru.yougile.com/api-v2"

    # Проверяем наличие данных для авторизации
    has_token = bool(Config.API_TOKEN)
    has_credentials = bool(Config.API_USERNAME and Config.API_PASSWORD)

    assert has_token or has_credentials, (
        "Не настроены данные для авторизации"
    )

    print(f"\nAPI Token configured: {bool(Config.API_TOKEN)}")
    print(
        f"Basic Auth configured: "
        f"{bool(Config.API_USERNAME and Config.API_PASSWORD)}"
    )
    if Config.TEST_COMPANY_ID:
        print(f"Company ID: {Config.TEST_COMPANY_ID}")
