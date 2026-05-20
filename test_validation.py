from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import time
import os

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

try:
    # Navigate to BicoLikha forgot password request page
    driver.get("http://127.0.0.1:8000/forgot-password/")
    time.sleep(2)

    # Enter an unregistered email to trigger input validation
    driver.find_element(By.NAME, "email").send_keys("nonexistent_user@example.com")
    
    # Submit form
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    
    # Assert validation error message is displayed
    if "This email address is not registered in our system." in driver.page_source:
        print("Validation Check - PASSED")
        os.makedirs("evidence", exist_ok=True)
        driver.save_screenshot("evidence/evidence_validation.png")
    else:
        print("Validation Check - FAILED (No error shown)")
        os.makedirs("evidence", exist_ok=True)
        driver.save_screenshot("evidence/evidence_validation_failed.png")

finally:
    driver.quit()