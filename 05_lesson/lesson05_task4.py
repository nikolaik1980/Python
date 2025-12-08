from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def simple_login():
    """Минималистичная версия выполнения задания"""

    # 1. Открыть Firefox
    driver = webdriver.Firefox()

    try:
        # 2. Перейти на страницу
        driver.get("http://the-internet.herokuapp.com/login")
        time.sleep(2)

        # 3. Ввести username
        driver.find_element(By.ID, "username").send_keys("tomsmith")

        # 4. Ввести password
        driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")

        # 5. Нажать кнопку Login
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Ждем появления сообщения
        time.sleep(2)

        # 6. Получить и вывести текст с зеленой плашки
        flash_message = driver.find_element(By.ID, "flash")
        message_text = flash_message.text.replace("×", "").strip()

        print("=" * 50)
        print("ТЕКСТ С ЗЕЛЕНОЙ ПЛАШКИ:")
        print("=" * 50)
        print(message_text)
        print("=" * 50)

        time.sleep(2)

    finally:
        # 7. Закрыть браузер
        driver.quit()
        print("\nБраузер закрыт")


if __name__ == "__main__":
    simple_login()