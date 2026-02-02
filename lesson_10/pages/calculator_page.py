"""
Page Object для страницы калькулятора
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from .base_page import BasePage
import allure


class CalculatorPage(BasePage):
    """
    Класс для работы со страницей калькулятора
    """

    # Локаторы элементов
    DELAY_INPUT = (By.CSS_SELECTOR, "input#delay")
    BUTTON_7 = (By.XPATH, "//span[text()='7']")
    BUTTON_PLUS = (By.XPATH, "//span[text()='+']")
    BUTTON_8 = (By.XPATH, "//span[text()='8']")
    BUTTON_EQUALS = (By.XPATH, "//span[text()='=']")
    RESULT = (By.CSS_SELECTOR, "div.screen")

    def __init__(self, driver):
        """
        Инициализация страницы калькулятора

        Args:
            driver: Экземпляр Selenium WebDriver
        """
        super().__init__(driver,
                         "https://bonigarcia.dev/selenium-webdriver-java"
                         "/slow-calculator.html")

    @allure.step("Установить задержку расчета: {delay} секунд")
    def set_delay(self, delay: str) -> None:
        """
        Устанавливает задержку расчета

        Args:
            delay: Значение задержки в секундах

        Returns:
            None
        """
        self.input_text(self.DELAY_INPUT, delay)

    @allure.step("Выполнить вычисление: 7 + 8")
    def calculate_7_plus_8(self) -> None:
        """
        Выполняет вычисление 7 + 8

        Returns:
            None
        """
        self.click_element(self.BUTTON_7)
        self.click_element(self.BUTTON_PLUS)
        self.click_element(self.BUTTON_8)
        self.click_element(self.BUTTON_EQUALS)

    def get_result(self) -> str:
        """
        Получает результат вычисления

        Returns:
            str: Текст результата
        """
        return self.get_text(self.RESULT)

    @allure.step("Ожидать результат вычисления с задержкой {delay} секунд")
    def wait_for_result_with_delay(self, delay: int) -> str:
        """
        Ожидает результат вычисления с учетом установленной задержки

        Args:
            delay: Задержка расчета в секундах

        Returns:
            str: Текст результата
        """
        # Ожидаем, что результат изменится на "15"
        # Добавляем небольшой запас времени для стабильности теста
        wait_time = delay + 2

        def result_is_calculated(driver):
            """Вспомогательная функция для ожидания результата."""
            result_text = self.get_result()
            return "15" in result_text

        # Используем явное ожидание
        WebDriverWait(self.driver, wait_time).until(
            lambda driver: result_is_calculated(driver)
        )

        return self.get_result()
