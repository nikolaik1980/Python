def test_calculator_with_45_second_delay():
    """
    Тест калькулятора с задержкой 45 секунд
    """
    from pages.calculator_page import CalculatorPage

    # Создаем драйвер Chrome
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Создаем объект страницы
        calculator_page = CalculatorPage(driver)

        # 1. Открыть страницу калькулятора
        calculator_page.open()

        # 2. Ввести значение 45 в поле задержки
        calculator_page.set_delay(45)

        # 3. Нажать кнопки: 7, +, 8, =
        calculator_page.calculate("7+8=")

        # 4. Проверить, что в окне отобразится результат 15 через 45 секунд
        result = calculator_page.wait_for_result("15")

        # Проверяем результат
        assert result == "15", f"Ожидался результат '15', получен '{result}'"

    finally:
        # Закрываем браузер
        driver.quit()


if __name__ == "__main__":
    test_calculator_with_45_second_delay()
