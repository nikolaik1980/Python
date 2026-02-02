"""
Page Object для страницы оформления заказа
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class CheckoutPage(BasePage):
    """
    Класс для работы со страницей оформления заказа

    Attributes:
        driver: Экземпляр Selenium WebDriver
    """

    # Локаторы для страницы информации
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    # Локаторы для страницы обзора
    SUMMARY_ITEMS = (By.CSS_SELECTOR, ".cart_item")
    ITEM_TOTAL = (By.CSS_SELECTOR, ".summary_subtotal_label")
    TAX = (By.CSS_SELECTOR, ".summary_tax_label")
    TOTAL = (By.CSS_SELECTOR, ".summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_CHECKOUT_BUTTON = (By.ID, "cancel")

    # Локаторы для страницы завершения
    COMPLETE_HEADER = (By.CSS_SELECTOR, ".complete-header")
    COMPLETE_TEXT = (By.CSS_SELECTOR, ".complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def __init__(self, driver):
        """
        Инициализация страницы оформления заказа

        Args:
            driver: Экземпляр Selenium WebDriver
        """
        super().__init__(
            driver,
            "https://www.saucedemo.com/checkout-step-one.html"
        )

    @allure.step("Заполнить информацию для заказа")
    def fill_checkout_information(
        self,
        first_name: str,
        last_name: str,
        postal_code: str
    ) -> None:
        """
        Заполняет форму с информацией для оформления заказа

        Args:
            first_name: Имя покупателя
            last_name: Фамилия покупателя
            postal_code: Почтовый индекс

        Returns:
            None
        """
        self.input_text(self.FIRST_NAME_INPUT, first_name)
        self.input_text(self.LAST_NAME_INPUT, last_name)
        self.input_text(self.POSTAL_CODE_INPUT, postal_code)

    @allure.step("Нажать кнопку 'Продолжить'")
    def continue_to_overview(self) -> None:
        """
        Нажимает кнопку "Continue" для перехода к обзору заказа

        Returns:
            None
        """
        self.click_element(self.CONTINUE_BUTTON)

    @allure.step("Нажать кнопку 'Отмена' на странице информации")
    def cancel_checkout(self) -> None:
        """
        Нажимает кнопку "Cancel" для отмены оформления заказа

        Returns:
            None
        """
        self.click_element(self.CANCEL_BUTTON)

    @allure.step("Получить сообщение об ошибке")
    def get_error_message(self) -> str:
        """
        Получает текст сообщения об ошибке при заполнении формы

        Returns:
            str: Текст сообщения об ошибке
        """
        return self.get_text(self.ERROR_MESSAGE)

    @allure.step("Получить количество товаров в обзоре заказа")
    def get_summary_item_count(self) -> int:
        """
        Получает количество товаров на странице обзора заказа

        Returns:
            int: Количество товаров
        """
        return len(self.find_elements(self.SUMMARY_ITEMS))

    @allure.step("Получить стоимость товаров")
    def get_item_total(self) -> float:
        """
        Получает общую стоимость товаров (без налога)

        Returns:
            float: Стоимость товаров
        """
        text = self.get_text(self.ITEM_TOTAL)
        # Извлекаем число из текста "Item total: $29.99"
        price_text = text.split('$')[1]
        return float(price_text)

    @allure.step("Получить сумму налога")
    def get_tax_amount(self) -> float:
        """
        Получает сумму налога

        Returns:
            float: Сумма налога
        """
        text = self.get_text(self.TAX)
        # Извлекаем число из текста "Tax: $2.40"
        price_text = text.split('$')[1]
        return float(price_text)

    @allure.step("Получить итоговую сумму")
    def get_total_amount(self) -> float:
        """
        Получает итоговую сумму к оплате

        Returns:
            float: Итоговая сумма
        """
        text = self.get_text(self.TOTAL)
        # Извлекаем число из текста "Total: $32.39"
        price_text = text.split('$')[1]
        return float(price_text)

    @allure.step("Нажать кнопку 'Завершить'")
    def finish_checkout(self) -> None:
        """
        Нажимает кнопку "Finish" для завершения оформления заказа

        Returns:
            None
        """
        self.click_element(self.FINISH_BUTTON)

    @allure.step("Нажать кнопку 'Отмена' на странице обзора")
    def cancel_checkout_from_overview(self) -> None:
        """
        Нажимает кнопку "Cancel" на странице обзора заказа

        Returns:
            None
        """
        self.click_element(self.CANCEL_CHECKOUT_BUTTON)

    @allure.step("Получить сообщение об успешном оформлении")
    def get_completion_message(self) -> str:
        """
        Получает сообщение об успешном оформлении заказа

        Returns:
            str: Текст сообщения
        """
        return self.get_text(self.COMPLETE_HEADER)

    @allure.step("Получить дополнительную информацию о заказе")
    def get_completion_text(self) -> str:
        """
        Получает дополнительный текст на странице завершения заказа

        Returns:
            str: Дополнительный текст
        """
        return self.get_text(self.COMPLETE_TEXT)

    @allure.step("Вернуться на главную страницу")
    def back_to_home(self) -> None:
        """
        Нажимает кнопку "Back Home" для возврата на главную страницу

        Returns:
            None
        """
        self.click_element(self.BACK_HOME_BUTTON)

    @allure.step("Выполнить полный процесс оформления заказа")
    def complete_checkout_process(
        self,
        first_name: str,
        last_name: str,
        postal_code: str
    ) -> str:
        """
        Выполняет полный процесс оформления заказа

        Args:
            first_name: Имя покупателя
            last_name: Фамилия покупателя
            postal_code: Почтовый индекс

        Returns:
            str: Сообщение об успешном оформлении
        """
        self.fill_checkout_information(first_name, last_name, postal_code)
        self.continue_to_overview()
        self.finish_checkout()
        return self.get_completion_message()

    @allure.step("Проверить корректность расчетов")
    def verify_calculations(self) -> bool:
        """
        Проверяет корректность расчетов на странице обзора заказа

        Returns:
            bool: True если расчеты корректны, False если нет
        """
        item_total = self.get_item_total()
        tax_amount = self.get_tax_amount()
        total_amount = self.get_total_amount()

        # Проверяем, что сумма товаров + налог = итоговая сумма
        calculated_total = round(item_total + tax_amount, 2)
        actual_total = round(total_amount, 2)

        return calculated_total == actual_total
