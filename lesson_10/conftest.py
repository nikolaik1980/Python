"""
Конфигурация тестов с настройкой Allure отчетов
"""

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    """
    Фикстура для инициализации и завершения работы драйвера Chrome

    Yields:
        WebDriver: Экземпляр Selenium WebDriver
    """
    with allure.step("Инициализация драйвера Chrome"):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_experimental_option(
            "excludeSwitches", ["enable-logging"]
        )

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)

    yield driver

    with allure.step("Закрытие драйвера"):
        driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для создания скриншотов при падении тестов

    Args:
        item: Объект теста
        call: Вызов теста
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            driver = item.funcargs['driver']
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Не удалось сделать скриншот: {e}")
