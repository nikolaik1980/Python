"""
Тесты для калькулятора с Allure отчетами
"""

import pytest
import allure
from pages.calculator_page import CalculatorPage


@allure.feature("Калькулятор")
@allure.severity(allure.severity_level.CRITICAL)
class TestCalculator:
    """
    Тестовый класс для проверки функциональности калькулятора
    """

    @allure.title("Тест медленного калькулятора с задержкой 45 секунд")
    @allure.description("""
    Тест проверяет работу калькулятора с установленной задержкой:
    1. Установить задержку 45 секунд
    2. Выполнить операцию 7 + 8
    3. Проверить, что результат появился через 45 секунд
    4. Проверить правильность результата
    """)
    def test_slow_calculator(self, driver):
        """
        Тест медленного калькулятора

        Args:
            driver: Фикстура с драйвером браузера
        """
        calculator_page = CalculatorPage(driver)

        with allure.step("Открыть страницу калькулятора"):
            calculator_page.open()

        with allure.step("Установить задержку расчета"):
            calculator_page.set_delay("45")

        with allure.step("Выполнить вычисление 7 + 8"):
            calculator_page.calculate_7_plus_8()

        with allure.step("Ожидать результат в течение 46 секунд"):
            import time
            time.sleep(46)

        with allure.step("Проверить результат вычисления"):
            result = calculator_page.get_result()
            assert "15" in result, f"Ожидался результат 15, получен: {result}"

    @allure.title("Тест калькулятора с задержкой 3 секунды")
    @allure.description("""
    Тест проверяет быстрый расчет калькулятора:
    1. Установить задержку 3 секунды
    2. Выполнить операцию 7 + 8
    3. Проверить результат через 4 секунды
    """)
    def test_fast_calculator(self, driver):
        """
        Тест быстрого калькулятора

        Args:
            driver: Фикстура с драйвером браузера
        """
        calculator_page = CalculatorPage(driver)

        with allure.step("Открыть страницу калькулятора"):
            calculator_page.open()

        with allure.step("Установить задержку 3 секунды"):
            calculator_page.set_delay("3")

        with allure.step("Выполнить вычисление 7 + 8"):
            calculator_page.calculate_7_plus_8()

        with allure.step("Ожидать результат 4 секунды"):
            import time
            time.sleep(4)

        with allure.step("Проверить результат вычисления"):
            result = calculator_page.get_result()
            assert "15" in result, f"Ожидался результат 15, получен: {result}"
