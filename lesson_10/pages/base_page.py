"""
Базовый класс Page Object для всех страниц
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class BasePage:
    """
    Базовый класс для всех страниц приложения

    Attributes:
        driver (WebDriver): Экземпляр Selenium WebDriver
        url (str): Базовый URL страницы
    """

    def __init__(self, driver, url: str = ""):
        """
        Инициализация базовой страницы

        Args:
            driver: Экземпляр Selenium WebDriver
            url: URL страницы (по умолчанию пустая строка)
        """
        self.driver = driver
        self.url = url

    def open(self) -> None:
        """
        Открывает страницу по указанному URL

        Returns:
            None
        """
        with allure.step(f"Открытие страницы: {self.url}"):
            self.driver.get(self.url)

    def find_element(self, locator: tuple, timeout: int = 10):
        """
        Находит элемент на странице с ожиданием

        Args:
            locator: Кортеж с методом поиска и значением локатора
            timeout: Время ожидания в секундах (по умолчанию 10)

        Returns:
            WebElement: Найденный элемент
        """
        with allure.step(f"Поиск элемента: {locator}"):
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )

    def find_elements(self, locator: tuple, timeout: int = 10) -> list:
        """
        Находит все элементы по локатору

        Args:
            locator: Кортеж с методом поиска и значением локатора
            timeout: Время ожидания в секундах (по умолчанию 10)

        Returns:
            list: Список найденных элементов
        """
        with allure.step(f"Поиск всех элементов: {locator}"):
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )

    def click_element(self, locator: tuple) -> None:
        """
        Кликает по элементу

        Args:
            locator: Кортеж с методом поиска и значением локатора

        Returns:
            None
        """
        with allure.step(f"Клик по элементу: {locator}"):
            element = self.find_element(locator)
            element.click()

    def input_text(self, locator: tuple, text: str) -> None:
        """
        Вводит текст в поле ввода

        Args:
            locator: Кортеж с методом поиска и значением локатора
            text: Текст для ввода

        Returns:
            None
        """
        with allure.step(f"Ввод текста '{text}' в элемент: {locator}"):
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        """
        Получает текст элемента

        Args:
            locator: Кортеж с методом поиска и значением локатора

        Returns:
            str: Текст элемента
        """
        with allure.step(f"Получение текста из элемента: {locator}"):
            return self.find_element(locator).text

    def is_element_visible(self, locator: tuple, timeout: int = 10) -> bool:
        """
        Проверяет видимость элемента

        Args:
            locator: Кортеж с методом поиска и значением локатора
            timeout: Время ожидания в секундах (по умолчанию 10)

        Returns:
            bool: True если элемент видим, False если нет
        """
        try:
            with allure.step(f"Проверка видимости элемента: {locator}"):
                WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(locator)
                )
                return True
        except:
            return False

    def switch_to_window(self, window_index: int) -> None:
        """
        Переключается на указанное окно браузера

        Args:
            window_index: Индекс окна

        Returns:
            None
        """
        with allure.step(f"Переключение на окно с индексом {window_index}"):
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[window_index])
