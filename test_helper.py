from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

def get_driver():
    options = webdriver.FirefoxOptions()
    # options.add_argument("--headless") # Uncomment this to run without a window opening
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    return driver