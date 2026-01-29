"""
Page Object для страницы авторизации
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class LoginPage(BasePage):
    """
    Класс для работы со страницей авторизации
    """

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver):
        """
        Инициализация страницы авторизации

        Args:
            driver: Экземпляр Selenium WebDriver
        """
        super().__init__(driver, "https://www.saucedemo.com/")

    @allure.step("Авторизация пользователя: {username}")
    def login(self, username: str, password: str) -> None:
        """
        Выполняет авторизацию пользователя

        Args:
            username: Имя пользователя
            password: Пароль

        Returns:
            None
        """
        self.input_text(self.USERNAME_INPUT, username)
        self.input_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """
        Получает текст сообщения об ошибке

        Returns:
            str: Текст ошибки
        """
        return self.get_text(self.ERROR_MESSAGE)
