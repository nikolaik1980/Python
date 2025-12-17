from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_calculator_slow_operation():
    # Инициализация драйвера для Chrome
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 50)  # Увеличиваем ожидание до 50 секунд

    try:
        # 1. Открыть страницу
        driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")

        # 2. Ввести значение 45 в поле delay
        delay_input = driver.find_element(By.CSS_SELECTOR, "#delay")
        delay_input.clear()
        delay_input.send_keys("45")

        # 3. Нажать кнопки: 7 + 8 =
        driver.find_element(By.XPATH, "//span[text()='7']").click()
        driver.find_element(By.XPATH, "//span[text()='+']").click()
        driver.find_element(By.XPATH, "//span[text()='8']").click()
        driver.find_element(By.XPATH, "//span[text()='=']").click()

        # 4. Проверить, что в окне отобразится результат 15 через 45 секунд
        # Ждем, пока прелоадер исчезнет (если есть)
        try:
            wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "spinner")))
        except:
            pass  # Если нет прелоадера, просто продолжаем

        # Ждем появления результата 15
        result_element = wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "screen"), "15")
        )

        # Получаем фактический результат для проверки и вывода в консоль
        result_display = driver.find_element(By.CLASS_NAME, "screen")
        actual_result = result_display.text

        # Assert проверка
        assert actual_result == "15", f"Ожидался результат 15, но получен {actual_result}"

        # Выводим сумму в консоль
        print(f"\nРезультат вычисления: {actual_result}")

    finally:
        driver.quit()