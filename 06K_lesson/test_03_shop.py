from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_shopping_cart_total():
    # Инициализация драйвера для Firefox
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 10)

    try:
        # 1. Открыть сайт магазина
        driver.get("https://www.saucedemo.com/")

        # 2. Авторизация
        username_field = driver.find_element(By.ID, "user-name")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")

        username_field.send_keys("standard_user")
        password_field.send_keys("secret_sauce")
        login_button.click()

        # 3. Добавить товары в корзину
        # Ждем загрузки страницы с товарами
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))

        # Добавляем Sauce Labs Backpack
        backpack_add_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        backpack_add_button.click()

        # Добавляем Sauce Labs Bolt T-Shirt
        tshirt_add_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
        tshirt_add_button.click()

        # Добавляем Sauce Labs Onesie
        onesie_add_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-onesie")
        onesie_add_button.click()

        # 4. Перейти в корзину
        cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()

        # 5. Нажать Checkout
        checkout_button = driver.find_element(By.ID, "checkout")
        checkout_button.click()

        # 6. Заполнить форму данными
        wait.until(EC.presence_of_element_located((By.ID, "first-name")))

        first_name_field = driver.find_element(By.ID, "first-name")
        last_name_field = driver.find_element(By.ID, "last-name")
        postal_code_field = driver.find_element(By.ID, "postal-code")

        first_name_field.send_keys("Николай")
        last_name_field.send_keys("Nikolay")
        postal_code_field.send_keys("446205")

        # 7. Нажать Continue
        continue_button = driver.find_element(By.ID, "continue")
        continue_button.click()

        # 8. Прочитать итоговую стоимость
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label")))

        total_element = driver.find_element(By.CLASS_NAME, "summary_total_label")
        total_text = total_element.text
        # Извлекаем сумму из текста "Total: $58.29"
        total_amount = total_text.split("$")[1]

        # 9. Вывести сумму в консоль
        print(f"Итоговая сумма: ${total_amount}")

        # 10. Проверить, что итоговая сумма равна $58.29
        assert total_amount == "58.29", f"Ожидалась сумма $58.29, но получено ${total_amount}"

        # Можно также проверить полный текст
        assert total_text == "Total: $58.29", f"Ожидалось 'Total: $58.29', но получено '{total_text}'"

    finally:
        # Закрыть браузер
        driver.quit()
