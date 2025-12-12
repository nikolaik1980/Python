from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def simple_ajax_task():
   
    driver = webdriver.Chrome()
    
    try:
        # 1. Переход на страницу
        driver.get("http://uitestingplayground.com/ajax")
        
        # 2. Нажатие на синюю кнопку
        button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "ajaxButton"))
        )
        button.click()
        
        # 3. Получение текста из зеленой плашки
        message = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "content"))
        )
        
        # Ждем появления текста
        WebDriverWait(driver, 20).until(
            lambda d: message.text.strip() != ""
        )
        
        # 4. Вывод текста в консоль
        text = message.text.strip()
        print(f'"{text}"')
        
    finally:
        driver.quit()

if __name__ == "__main__":
    simple_ajax_task()


