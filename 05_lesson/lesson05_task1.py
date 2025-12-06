from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def click_blue_button():
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    try:
        driver.get("http://uitestingplayground.com/classattr")
        
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-primary"))
        )
        button.click()
        
        try:
            alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
            print(f"Alert text: {alert.text}")
            alert.accept()
        except:
            print("No alert found")
            
    finally:
        time.sleep(3)  # Пауза перед закрытием
        driver.quit()

if __name__ == "__main__":
    click_blue_button()