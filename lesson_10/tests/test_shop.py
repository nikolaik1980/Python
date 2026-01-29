"""
Тесты для интернет-магазина с Allure отчетами
"""

import pytest
import allure
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.feature("Интернет-магазин")
@allure.severity(allure.severity_level.CRITICAL)
class TestShop:
    """
    Тестовый класс для проверки функциональности интернет-магазина
    """

    @allure.title("Тест успешной авторизации")
    @allure.description("""
    Тест проверяет успешную авторизацию стандартного пользователя:
    1. Открыть страницу авторизации
    2. Ввести корректные учетные данные
    3. Проверить переход на главную страницу
    """)
    def test_successful_login(self, driver):
        """
        Тест успешной авторизации

        Args:
            driver: Фикстура с драйвером браузера
        """
        login_page = LoginPage(driver)

        with allure.step("Открыть страницу авторизации"):
            login_page.open()

        with allure.step("Выполнить авторизацию"):
            login_page.login("standard_user", "secret_sauce")

        with allure.step("Проверить успешный вход"):
            main_page = MainPage(driver)
            error_msg = "Товары не отображаются после входа"
            assert main_page.are_products_displayed(), error_msg
            error_msg = "Неверный заголовок страницы"
            assert "Products" in main_page.get_page_title(), error_msg

    @allure.title("Тест добавления товара в корзину")
    @allure.description("""
    Тест проверяет добавление товара в корзину:
    1. Авторизоваться
    2. Добавить товар в корзину
    3. Проверить обновление счетчика корзины
    4. Перейти в корзину и проверить наличие товара
    """)
    def test_add_to_cart(self, driver):
        """
        Тест добавления товара в корзину

        Args:
            driver: Фикстура с драйвером браузера
        """
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        main_page = MainPage(driver)

        with allure.step("Получить информацию о первом товаре"):
            product_info = main_page.get_product_info_by_index(0)
            product_name = product_info['name']

        with allure.step("Добавить товар в корзину"):
            main_page.add_product_to_cart_by_index(0)

        with allure.step("Проверить счетчик корзины"):
            cart_count = main_page.get_cart_badge_count()
            error_msg = f"Ожидалось 1 товар в корзине, получено: {cart_count}"
            assert cart_count == 1, error_msg

        with allure.step("Перейти в корзину"):
            main_page.go_to_cart()

        with allure.step("Проверить наличие товара в корзине"):
            cart_page = CartPage(driver)
            error_msg = f"Товар {product_name} не найден в корзине"
            assert cart_page.is_item_in_cart(product_name), error_msg

    @allure.title("Тест оформления заказа")
    @allure.description("""
    Тест проверяет полный процесс оформления заказа:
    1. Авторизоваться
    2. Добавить товары в корзину
    3. Перейти в корзину
    4. Начать оформление заказа
    5. Заполнить информацию
    6. Завершить заказ
    """)
    def test_checkout_process(self, driver):
        """
        Тест процесса оформления заказа

        Args:
            driver: Фикстура с драйвером браузера
        """
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        main_page = MainPage(driver)

        with allure.step("Добавить несколько товаров в корзину"):
            main_page.add_product_to_cart_by_index(0)
            main_page.add_product_to_cart_by_index(1)

        with allure.step("Перейти в корзину"):
            main_page.go_to_cart()

        cart_page = CartPage(driver)

        with allure.step("Начать оформление заказа"):
            cart_page.proceed_to_checkout()

        checkout_page = CheckoutPage(driver)

        with allure.step("Заполнить информацию для заказа"):
            checkout_page.fill_checkout_information(
                "Иван",
                "Иванов",
                "123456"
            )
            checkout_page.continue_to_overview()

        with allure.step("Проверить корректность расчетов"):
            error_msg = "Расчеты на странице обзора некорректны"
            assert checkout_page.verify_calculations(), error_msg

        with allure.step("Завершить оформление заказа"):
            checkout_page.finish_checkout()

        with allure.step("Проверить сообщение об успешном оформлении"):
            message = checkout_page.get_completion_message()
            error_msg = f"Неверное сообщение об успехе: {message}"
            assert "Thank you for your order" in message, error_msg

    @allure.title("Тест сортировки товаров")
    @allure.description("""
    Тест проверяет сортировку товаров по разным параметрам:
    1. Проверить сортировку по имени (A-Z)
    2. Проверить сортировку по имени (Z-A)
    3. Проверить сортировку по цене (низкая-высокая)
    4. Проверить сортировку по цене (высокая-низкая)
    """)
    @pytest.mark.parametrize("sort_option,expected_order", [
        ("az", True),
        ("za", False),
        ("lohi", True),
        ("hilo", False)
    ])
    def test_product_sorting(self, driver, sort_option, expected_order):
        """
        Тест сортировки товаров

        Args:
            driver: Фикстура с драйвером браузера
            sort_option: Параметр сортировки
            expected_order: Ожидаемый порядок (True - прямой, False - обратный)
        """
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        main_page = MainPage(driver)

        step_msg = f"Применить сортировку: {sort_option}"
        with allure.step(step_msg):
            main_page.sort_products(sort_option)

        with allure.step("Проверить порядок товаров"):
            if sort_option in ["az", "za"]:
                # Проверка сортировки по имени
                product_names = main_page.get_all_product_names()
                reverse_order = not expected_order
                sorted_names = sorted(product_names, reverse=reverse_order)
                error_msg = "Сортировка по имени работает некорректно"
                assert product_names == sorted_names, error_msg
            else:
                # Проверка сортировки по цене
                product_prices = main_page.get_all_product_prices()
                reverse_order = not expected_order
                sorted_prices = sorted(product_prices, reverse=reverse_order)
                error_msg = "Сортировка по цене работает некорректно"
                assert product_prices == sorted_prices, error_msg

    @allure.title("Тест удаления товара из корзины")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
    Тест проверяет удаление товара из корзины:
    1. Добавить товар в корзину
    2. Перейти в корзину
    3. Удалить товар
    4. Проверить, что корзина пуста
    """)
    def test_remove_from_cart(self, driver):
        """
        Тест удаления товара из корзины

        Args:
            driver: Фикстура с драйвером браузера
        """
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        main_page = MainPage(driver)

        with allure.step("Добавить товар в корзину"):
            main_page.add_product_to_cart_by_index(0)
            product_info = main_page.get_product_info_by_index(0)
            product_name = product_info['name']

        with allure.step("Перейти в корзину"):
            main_page.go_to_cart()

        cart_page = CartPage(driver)

        with allure.step("Проверить наличие товара в корзине"):
            error_msg = "Товар не добавлен в корзину"
            assert cart_page.is_item_in_cart(product_name), error_msg

        with allure.step("Удалить товар из корзины"):
            cart_page.remove_item_by_name(product_name)

        with allure.step("Проверить, что корзина пуста"):
            error_msg = "Корзина не пуста после удаления товара"
            assert cart_page.is_cart_empty(), error_msg

    @allure.title("Тест выхода из системы")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
    Тест проверяет выход из системы:
    1. Авторизоваться
    2. Выполнить выход
    3. Проверить, что произошел возврат на страницу авторизации
    """)
    def test_logout(self, driver):
        """
        Тест выхода из системы

        Args:
            driver: Фикстура с драйвером браузера
        """
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        main_page = MainPage(driver)

        with allure.step("Выполнить выход из системы"):
            main_page.logout()

        with allure.step("Проверить форму авторизации"):
            error_msg = "Не удалось выйти из системы"
            element_visible = login_page.is_element_visible(
                login_page.LOGIN_BUTTON
            )
            assert element_visible, error_msg
