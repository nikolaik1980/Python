from selenium.webdriver.common.by import By


class CartPage:
    def __init__(self, driver):
        self.driver = driver

    def click_checkout(self):
        checkout_button = self.driver.find_element(By.ID, "checkout")
        checkout_button.click()

    def get_cart_items_count(self):
        cart_badge = self.driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        if cart_badge:
            return int(cart_badge[0].text)
        return 0