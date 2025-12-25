from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def add_product_to_cart(self, product_id):
        add_button = self.driver.find_element(By.ID, f"add-to-cart-{product_id}")
        add_button.click()

    def add_products_to_cart(self, product_ids):
        for product_id in product_ids:
            self.add_product_to_cart(product_id)

    def go_to_cart(self):
        cart_icon = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()

        # Ждем загрузки страницы корзины
        self.wait.until(EC.presence_of_element_located((By.ID, "checkout")))