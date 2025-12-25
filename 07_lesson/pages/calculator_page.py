from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    """Page Object для страницы калькулятора"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 50)

    def open(self):
        """Открыть страницу калькулятора"""
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
        return self

    def set_delay(self, delay):
        """Установить значение задержки"""
        delay_input = self.driver.find_element(By.ID, "delay")
        delay_input.clear()
        delay_input.send_keys(str(delay))
        return self

    def click_button(self, button_text):
        """Нажать кнопку калькулятора по тексту"""
        button = self.driver.find_element(By.XPATH, f"//span[text()='{button_text}']")
        button.click()
        return self

    def calculate(self, expression):
        """Выполнить вычисление по выражению"""
        for char in expression:
            self.click_button(char)
        return self

    def get_result(self):
        """Получить результат с дисплея"""
        screen = self.driver.find_element(By.CLASS_NAME, "screen")
        return screen.text

    def wait_for_result(self, expected_result):
        """Ожидать появления результата"""
        self.wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "screen"), str(expected_result))
        )
        return self.get_result()