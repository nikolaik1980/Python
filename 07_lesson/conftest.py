import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


@pytest.fixture
def chrome_driver():
    """Фикстура для Chrome драйвера"""
    options = ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def firefox_driver():
    """Фикстура для Firefox драйвера"""
    options = FirefoxOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Firefox(options=options)
    yield driver
    driver.quit()