from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def simple_input_task():
    """Простая версия выполнения задания"""

    # 1. Открыть Firefox
    driver = webdriver.Firefox()

    try:
        # 2. Перейти на страницу
        driver.get("http://the-internet.herokuapp.com/inputs")
        time.sleep(2)

        # 3. Найти поле ввода
        input_field = driver.find_element(By.TAG_NAME, "input")

        # 4. Ввести "Sky"
        input_field.send_keys("Sky")
        print("Введен текст: Sky")
        time.sleep(1)

        # 5. Очистить поле
        input_field.clear()
        print("Поле очищено")
        time.sleep(1)

        # 6. Ввести "Pro"
        input_field.send_keys("Pro")
        print("Введен текст: Pro")
        time.sleep(2)

    finally:
        # 7. Закрыть браузер
        driver.quit()
        print("Браузер закрыт")


if __name__ == "__main__":
    simple_input_task()