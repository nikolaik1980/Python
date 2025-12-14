from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_form_validation():
    # Инициализация драйвера для Edge
    driver = webdriver.Edge()
    wait = WebDriverWait(driver, 10)

    try:
        # 1. Открыть страницу
        driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")

        # 2. Заполнить форму
        driver.find_element(By.CSS_SELECTOR, 'input[name="first-name"]').send_keys("Иван")
        driver.find_element(By.CSS_SELECTOR, 'input[name="last-name"]').send_keys("Петров")
        driver.find_element(By.CSS_SELECTOR, 'input[name="address"]').send_keys("Ленина, 55-3")
        driver.find_element(By.CSS_SELECTOR, 'input[name="e-mail"]').send_keys("test@skypro.com")
        driver.find_element(By.CSS_SELECTOR, 'input[name="phone"]').send_keys("+7985899998787")
        # Zip code оставляем пустым
        driver.find_element(By.CSS_SELECTOR, 'input[name="city"]').send_keys("Москва")
        driver.find_element(By.CSS_SELECTOR, 'input[name="country"]').send_keys("Россия")
        driver.find_element(By.CSS_SELECTOR, 'input[name="job-position"]').send_keys("QA")
        driver.find_element(By.CSS_SELECTOR, 'input[name="company"]').send_keys("SkyPro")

        # 3. Нажать кнопку Submit
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()

        # 4. Проверить, что поле Zip code подсвечено красным
        zip_code_field = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="zip-code"]'))
        )
        # Проверяем наличие класса invalid (обычно красное подсвечивание)
        assert "is-invalid" in zip_code_field.get_attribute("class"), "Поле Zip code должно быть подсвечено красным"

        # 5. Проверить, что остальные поля подсвечены зеленым
        green_fields = [
            'input[name="first-name"]',
            'input[name="last-name"]',
            'input[name="address"]',
            'input[name="e-mail"]',
            'input[name="phone"]',
            'input[name="city"]',
            'input[name="country"]',
            'input[name="job-position"]',
            'input[name="company"]'
        ]

        for field_selector in green_fields:
            field = driver.find_element(By.CSS_SELECTOR, field_selector)
            # Проверяем наличие класса valid (обычно зеленое подсвечивание)
            assert "is-valid" in field.get_attribute("class"), f"Поле {field_selector} должно быть подсвечено зеленым"

    finally:
        driver.quit()