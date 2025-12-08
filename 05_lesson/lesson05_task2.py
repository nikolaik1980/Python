from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def click_dynamic_button():
    """Простая и надежная версия для клика по кнопке с динамическим ID"""

    driver = webdriver.Chrome()

    try:
        # 1. Открываем страницу
        driver.get("http://uitestingplayground.com/dynamicid")

        # 2. Ждем загрузки кнопки
        wait = WebDriverWait(driver, 10)

        # 3. Ищем кнопку по сочетанию класса и текста (самый надежный способ)
        # CSS селектор: кнопка с классом btn-primary
        button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary"))
        )

        # 4. Выполняем клик
        button.click()
        print("Успешный клик по кнопке с динамическим ID!")

        # 5. Пауза для наблюдения результата
        time.sleep(2)

    finally:
        driver.quit()


if __name__ == "__main__":
    # Запускаем функцию
    click_dynamic_button()