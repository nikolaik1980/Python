from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def simple_text_input_task():
   
    driver = webdriver.Chrome()
    
    try:
        # 1. Переход на страницу
        driver.get("http://uitestingplayground.com/textinput")
        
        # 2. Ввод текста SkyPro
        text_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "newButtonName"))
        )
        text_input.clear()
        text_input.send_keys("SkyPro")
        
        # 3. Нажатие на синюю кнопку
        button = driver.find_element(By.ID, "updatingButton")
        button.click()
        
        # 4. Получение текста кнопки и вывод в консоль
        # Ждем, пока текст кнопки изменится
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "updatingButton"), "SkyPro")
        )
        
        # Получаем текст кнопки
        updated_button = driver.find_element(By.ID, "updatingButton")
        button_text = updated_button.text.strip()
        
        # Выводим в консоль
        print(f'"{button_text}"')
        
    finally:
        driver.quit()

if __name__ == "__main__":
    simple_text_input_task()


