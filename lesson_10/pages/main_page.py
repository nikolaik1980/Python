"""
Page Object для главной страницы интернет-магазина
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import allure


class MainPage(BasePage):
    """
    Класс для работы с главной страницей интернет-магазина

    Attributes:
        driver: Экземпляр Selenium WebDriver
    """

    # Локаторы элементов
    PRODUCTS_TITLE = (By.CSS_SELECTOR, ".title")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".inventory_item")
    PRODUCT_NAME = (By.CSS_SELECTOR, ".inventory_item_name")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".inventory_item_price")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button.btn_inventory")
    REMOVE_FROM_CART_BUTTON = (By.CSS_SELECTOR, "button.btn_inventory")
    SHOPPING_CART_LINK = (By.CSS_SELECTOR, ".shopping_cart_link")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")
    SORT_DROPDOWN = (By.CSS_SELECTOR, ".product_sort_container")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        """
        Инициализация главной страницы

        Args:
            driver: Экземпляр Selenium WebDriver
        """
        super().__init__(driver,
                         "https://www.saucedemo.com/inventory.html")

    @allure.step("Получить заголовок страницы товаров")
    def get_page_title(self) -> str:
        """
        Получает заголовок страницы с товарами

        Returns:
            str: Текст заголовка
        """
        return self.get_text(self.PRODUCTS_TITLE)

    @allure.step("Получить количество товаров на странице")
    def get_product_count(self) -> int:
        """
        Получает количество товаров на странице

        Returns:
            int: Количество товаров
        """
        return len(self.find_elements(self.PRODUCT_ITEMS))

    @allure.step("Получить названия всех товаров")
    def get_all_product_names(self) -> list:
        """
        Получает список названий всех товаров на странице

        Returns:
            list: Список названий товаров
        """
        products = self.find_elements(self.PRODUCT_NAME)
        return [product.text for product in products]

    @allure.step("Получить цены всех товаров")
    def get_all_product_prices(self) -> list:
        """
        Получает список цен всех товаров на странице

        Returns:
            list: Список цен товаров
        """
        products = self.find_elements(self.PRODUCT_PRICE)
        return [float(product.text.replace('$', '')) for product in products]

    @allure.step("Добавить товар в корзину по индексу: {product_index}")
    def add_product_to_cart_by_index(self, product_index: int) -> None:
        """
        Добавляет товар в корзину по указанному индексу

        Args:
            product_index: Индекс товара (начиная с 0)

        Returns:
            None
        """
        add_buttons = self.find_elements(self.ADD_TO_CART_BUTTON)
        if product_index < len(add_buttons):
            add_buttons[product_index].click()

    @allure.step("Добавить товар в корзину по названию: {product_name}")
    def add_product_to_cart_by_name(self, product_name: str) -> None:
        """
        Добавляет товар в корзину по названию

        Args:
            product_name: Название товара

        Returns:
            None
        """
        product_items = self.find_elements(self.PRODUCT_ITEMS)
        for index, item in enumerate(product_items):
            name_element = item.find_element(*self.PRODUCT_NAME)
            if name_element.text == product_name:
                add_button = item.find_element(*self.ADD_TO_CART_BUTTON)
                add_button.click()
                break

    @allure.step("Удалить товар из корзины по индексу: {product_index}")
    def remove_product_from_cart_by_index(self, product_index: int) -> None:
        """
        Удаляет товар из корзины по указанному индексу

        Args:
            product_index: Индекс товара (начиная с 0)

        Returns:
            None
        """
        remove_buttons = self.find_elements(self.REMOVE_FROM_CART_BUTTON)
        if product_index < len(remove_buttons):
            # Проверяем, что кнопка действительно для удаления
            button = remove_buttons[product_index]
            if button.text.lower() == "remove":
                button.click()

    @allure.step("Перейти в корзину")
    def go_to_cart(self) -> None:
        """
        Переходит на страницу корзины

        Returns:
            None
        """
        self.click_element(self.SHOPPING_CART_LINK)

    @allure.step("Получить количество товаров в корзине из бейджа")
    def get_cart_badge_count(self) -> int:
        """
        Получает количество товаров в корзине из бейджа

        Returns:
            int: Количество товаров в корзине (0 если бейдж отсутствует)
        """
        try:
            badge = self.find_element(self.CART_BADGE, timeout=2)
            return int(badge.text)
        except Exception:
            return 0

    @allure.step("Сортировать товары по: {sort_option}")
    def sort_products(self, sort_option: str) -> None:
        """
        Сортирует товары по указанному параметру

        Args:
            sort_option: Вариант сортировки:
                - "az" (Name A to Z)
                - "za" (Name Z to A)
                - "lohi" (Price low to high)
                - "hilo" (Price high to low)

        Returns:
            None
        """
        from selenium.webdriver.support.select import Select

        dropdown = self.find_element(self.SORT_DROPDOWN)
        select = Select(dropdown)
        select.select_by_value(sort_option)

    @allure.step("Открыть меню")
    def open_menu(self) -> None:
        """
        Открывает боковое меню

        Returns:
            None
        """
        self.click_element(self.MENU_BUTTON)

    @allure.step("Выполнить выход из системы")
    def logout(self) -> None:
        """
        Выполняет выход из системы через боковое меню

        Returns:
            None
        """
        self.open_menu()

        # Явное ожидание появления меню
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK))

        self.click_element(self.LOGOUT_LINK)

    @allure.step("Получить информацию о товаре по индексу: {product_index}")
    def get_product_info_by_index(self, product_index: int) -> dict:
        """
        Получает полную информацию о товаре по индексу

        Args:
            product_index: Индекс товара (начиная с 0)

        Returns:
            dict: Словарь с информацией о товаре
                - name: Название товара
                - price: Цена товара
                - description: Описание товара
                - button_text: Текст кнопки
        """
        product_items = self.find_elements(self.PRODUCT_ITEMS)
        if product_index >= len(product_items):
            return {}

        item = product_items[product_index]
        info = {
            'name': item.find_element(*self.PRODUCT_NAME).text,
            'price': item.find_element(*self.PRODUCT_PRICE).text,
            'description': item.find_element(
                By.CSS_SELECTOR, ".inventory_item_desc"
            ).text,
            'button_text': item.find_element(*self.ADD_TO_CART_BUTTON).text
        }
        return info

    @allure.step("Добавить несколько товаров в корзину")
    def add_multiple_products_to_cart(self, product_indices: list) -> None:
        """
        Добавляет несколько товаров в корзину

        Args:
            product_indices: Список индексов товаров для добавления

        Returns:
            None
        """
        for index in product_indices:
            self.add_product_to_cart_by_index(index)

    @allure.step("Проверить, есть ли товары на странице")
    def are_products_displayed(self) -> bool:
        """
        Проверяет, отображаются ли товары на странице

        Returns:
            bool: True если товары отображаются, False если нет
        """
        return self.is_element_visible(self.PRODUCT_ITEMS)
