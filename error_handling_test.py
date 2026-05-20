from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import time
import os

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

try:
    driver.get("http://127.0.0.1:8000/accounts/login/")
    time.sleep(2)
    
    # Test Error Handling: Invalid Login
    driver.find_element(By.NAME, "username").send_keys("invalid_user_999@example.com")
    driver.find_element(By.NAME, "password").send_keys("wrongpassword")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    time.sleep(2)
    
    # Verify that the system handles the error gracefully and shows the login issue message
    if "Please enter a correct username and password" in driver.page_source or "Sign in issue" in driver.page_source:
        print("Error Handling (Invalid Login) - PASSED")
        os.makedirs("evidence", exist_ok=True)
        driver.save_screenshot("evidence/evidence_error_handling.png")
    else:
        print("Error Handling (Invalid Login) - FAILED")
        os.makedirs("evidence", exist_ok=True)
        driver.save_screenshot("evidence/evidence_error_handling_failed.png")

finally:
    driver.quit()

