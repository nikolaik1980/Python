from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def fill_shipping_info(self, first_name, last_name, postal_code):
        self.wait.until(EC.presence_of_element_located((By.ID, "first-name")))

        first_name_field = self.driver.find_element(By.ID, "first-name")
        last_name_field = self.driver.find_element(By.ID, "last-name")
        postal_code_field = self.driver.find_element(By.ID, "postal-code")

        first_name_field.send_keys(first_name)
        last_name_field.send_keys(last_name)
        postal_code_field.send_keys(postal_code)

    def continue_to_overview(self):
        continue_button = self.driver.find_element(By.ID, "continue")
        continue_button.click()

        # Ждем загрузки страницы с итогами
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label")))

    def get_total_amount(self):
        total_element = self.driver.find_element(By.CLASS_NAME, "summary_total_label")
        total_text = total_element.text
        return total_text.split("$")[1]

    def get_total_text(self):
        total_element = self.driver.find_element(By.CLASS_NAME, "summary_total_label")
        return total_element.text