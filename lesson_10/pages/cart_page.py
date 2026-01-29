"""
Page Object для страницы корзины покупок
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class CartPage(BasePage):
    """
    Класс для работы со страницей корзины покупок

    Attributes:
        driver: Экземпляр Selenium WebDriver
    """

    # Локаторы элементов
    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")
    ITEM_NAME = (By.CSS_SELECTOR, ".inventory_item_name")
    ITEM_PRICE = (By.CSS_SELECTOR, ".inventory_item_price")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button.cart_button")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CART_QUANTITY = (By.CSS_SELECTOR, ".cart_quantity")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")

    def __init__(self, driver):
        """
        Инициализация страницы корзины

        Args:
            driver: Экземпляр Selenium WebDriver
        """
        super().__init__(driver, "https://www.saucedemo.com/cart.html")

    @allure.step("Получить количество товаров в корзине")
    def get_cart_item_count(self) -> int:
        """
        Получает количество товаров в корзине

        Returns:
            int: Количество товаров
        """
        return len(self.find_elements(self.CART_ITEMS))

    @allure.step("Получить названия всех товаров в корзине")
    def get_all_item_names(self) -> list:
        """
        Получает список названий всех товаров в корзине

        Returns:
            list: Список названий товаров
        """
        items = self.find_elements(self.ITEM_NAME)
        return [item.text for item in items]

    @allure.step("Получить цены всех товаров в корзине")
    def get_all_item_prices(self) -> list:
        """
        Получает список цен всех товаров в корзине

        Returns:
            list: Список цен товаров
        """
        items = self.find_elements(self.ITEM_PRICE)
        return [float(item.text.replace('$', '')) for item in items]

    @allure.step("Удалить товар из корзины по индексу: {item_index}")
    def remove_item_by_index(self, item_index: int) -> None:
        """
        Удаляет товар из корзины по указанному индексу

        Args:
            item_index: Индекс товара для удаления (начиная с 0)

        Returns:
            None
        """
        remove_buttons = self.find_elements(self.REMOVE_BUTTON)
        if item_index < len(remove_buttons):
            remove_buttons[item_index].click()

    @allure.step("Удалить товар по названию: {item_name}")
    def remove_item_by_name(self, item_name: str) -> None:
        """
        Удаляет товар из корзины по названию

        Args:
            item_name: Название товара для удаления

        Returns:
            None
        """
        cart_items = self.find_elements(self.CART_ITEMS)
        for index, item in enumerate(cart_items):
            name_element = item.find_element(*self.ITEM_NAME)
            if name_element.text == item_name:
                remove_button = item.find_element(*self.REMOVE_BUTTON)
                remove_button.click()
                break

    @allure.step("Нажать кнопку 'Продолжить покупки'")
    def continue_shopping(self) -> None:
        """
        Нажимает кнопку "Continue Shopping"

        Returns:
            None
        """
        self.click_element(self.CONTINUE_SHOPPING_BUTTON)

    @allure.step("Нажать кнопку 'Оформить заказ'")
    def proceed_to_checkout(self) -> None:
        """
        Нажимает кнопку "Checkout" для перехода к оформлению заказа

        Returns:
            None
        """
        self.click_element(self.CHECKOUT_BUTTON)

    @allure.step("Проверить, что корзина пуста")
    def is_cart_empty(self) -> bool:
        """
        Проверяет, пуста ли корзина

        Returns:
            bool: True если корзина пуста, False если нет
        """
        try:
            # Проверяем наличие бейджа с количеством товаров
            badge = self.find_element(self.CART_BADGE, timeout=2)
            return False
        except:
            # Проверяем наличие товаров в корзине
            items = self.find_elements(self.CART_ITEMS)
            return len(items) == 0

    @allure.step("Получить общую стоимость товаров в корзине")
    def get_total_price(self) -> float:
        """
        Вычисляет общую стоимость всех товаров в корзине

        Returns:
            float: Общая стоимость
        """
        prices = self.get_all_item_prices()
        return sum(prices)

    @allure.step("Очистить всю корзину")
    def clear_cart(self) -> None:
        """
        Удаляет все товары из корзины

        Returns:
            None
        """
        remove_buttons = self.find_elements(self.REMOVE_BUTTON)
        for button in remove_buttons:
            button.click()

    @allure.step("Проверить наличие товара в корзине: {item_name}")
    def is_item_in_cart(self, item_name: str) -> bool:
        """
        Проверяет наличие товара с указанным названием в корзине

        Args:
            item_name: Название товара для проверки

        Returns:
            bool: True если товар найден, False если нет
        """
        item_names = self.get_all_item_names()
        return item_name in item_names

    @allure.step("Получить количество конкретного товара")
    def get_item_quantity(self, item_name: str) -> int:
        """
        Получает количество указанного товара в корзине

        Args:
            item_name: Название товара

        Returns:
            int: Количество товара (если товар не найден, возвращает 0)
        """
        cart_items = self.find_elements(self.CART_ITEMS)
        for item in cart_items:
            name_element = item.find_element(*self.ITEM_NAME)
            if name_element.text == item_name:
                try:
                    quantity_element = item.find_element(*self.CART_QUANTITY)
                    return int(quantity_element.text)
                except:
                    return 1
        return 0
