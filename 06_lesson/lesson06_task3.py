from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

def simple_wait_for_images():
   
    driver = webdriver.Chrome()
    
    try:
        # 1. Переход на страницу
        driver.get("https://bonigarcia.dev/selenium-webdriver-java/loading-images.html")
        
        # 2. Ожидание загрузки всех картинок
        print("Ожидаю загрузку картинок...")
        
        # Ждем появления 4 картинок в контейнере
        wait = WebDriverWait(driver, 30)
        
        # Ждем, пока будет хотя бы 4 картинки
        wait.until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, "#image-container img")) >= 4
        )
        
        # Ждем, пока все картинки загрузятся
        def all_images_loaded(driver):
            images = driver.find_elements(By.CSS_SELECTOR, "#image-container img")
            if len(images) < 4:
                return False
            
            for img in images:
                # Проверяем через JavaScript, загрузилась ли картинка
                is_loaded = driver.execute_script("""
                    return arguments[0].complete && 
                           arguments[0].naturalWidth > 0 && 
                           arguments[0].src !== "";
                """, img)
                
                if not is_loaded:
                    return False
            
            return True
        
        wait.until(all_images_loaded)
        print("Все картинки загружены")
        
        # 3. Получение значения атрибута src у 3-й картинки
        images = driver.find_elements(By.CSS_SELECTOR, "#image-container img")
        
        if len(images) >= 3:
            third_image = images[2]  # 3-я картинка (индекс 2)
            src_value = third_image.get_attribute("src")
            
            # 4. Вывод значения в консоль
            print(f"\nSrc 3-й картинки:")
            print("-" * 80)
            print(src_value)
            print("-" * 80)
        else:
            print(f"Ошибка: найдено только {len(images)} картинок")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    simple_wait_for_images()

