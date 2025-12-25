from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find(self, *locator):
        return self.driver.find_element(*locator)

    def click(self, *locator):
        self.find(*locator).click()

    def send_keys(self, text, *locator):
        element = self.find(*locator)
        element.clear()
        element.send_keys(text)