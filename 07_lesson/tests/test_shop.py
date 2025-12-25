import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class TestShoppingCart:
    @pytest.fixture(scope="function")
    def setup(self):
        # Инициализация драйвера Firefox
        driver = webdriver.Firefox()
        driver.maximize_window()
        yield driver
        # Закрытие браузера после теста
        driver.quit()

    def test_shopping_cart_total(self, setup):
        driver = setup

        # Использование Page Object
        login_page = LoginPage(driver)
        main_page = MainPage(driver)
        cart_page = CartPage(driver)
        checkout_page = CheckoutPage(driver)

        # 1. Открыть сайт и авторизоваться
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        # 2. Добавить товары в корзину
        products_to_add = [
            "sauce-labs-backpack",
            "sauce-labs-bolt-t-shirt",
            "sauce-labs-onesie"
        ]
        main_page.add_products_to_cart(products_to_add)

        # 3. Перейти в корзину
        main_page.go_to_cart()

        # 4. Начать оформление заказа
        cart_page.click_checkout()

        # 5. Заполнить информацию о доставке
        checkout_page.fill_shipping_info("Николай", "Nikolay", "446205")

        # 6. Перейти к обзору заказа
        checkout_page.continue_to_overview()

        # 7. Проверить итоговую сумму
        total_amount = checkout_page.get_total_amount()
        total_text = checkout_page.get_total_text()

        # 8. Вывести сумму в консоль
        print(f"Итоговая сумма: ${total_amount}")

        # 9. Проверки
        assert total_amount == "58.29", f"Ожидалась сумма $58.29, но получено ${total_amount}"
        assert total_text == "Total: $58.29", f"Ожидалось 'Total: $58.29', но получено '{total_text}'"

        # Дополнительная проверка количества товаров в корзине
        assert cart_page.get_cart_items_count() == 3, f"Ожидалось 3 товара в корзине"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])