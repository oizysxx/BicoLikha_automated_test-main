from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import time
import random
import os

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

try:
    # 1. Sign up a new randomized user
    driver.get("http://127.0.0.1:8000/signup/")
    time.sleep(2)
    
    # Generate randomized customer details
    random_id = random.randint(1000, 9999)
    test_email = f"customer_{random_id}@example.com"
    test_phone = f"0917{random.randint(1000000, 9999999)}"
    test_pass = "Password123"

    # Fill out signup form
    driver.find_element(By.NAME, "first_name").send_keys("Automated")
    driver.find_element(By.NAME, "last_name").send_keys(f"User{random_id}")
    driver.find_element(By.NAME, "email").send_keys(test_email)
    driver.find_element(By.NAME, "phone_number").send_keys(test_phone)
    driver.find_element(By.NAME, "password").send_keys(test_pass)
    
    # Click policy checkbox
    driver.find_element(By.ID, "policy").click()
    
    # Submit the form
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(3) # Wait for redirects/automatic login

    # Check if we logged in and redirected to catalog home page
    # Since signup automatically logs in and redirects to '/' or 'http://127.0.0.1:8000/'
    current_url = driver.current_url.rstrip('/')
    if current_url == "http://127.0.0.1:8000" or current_url == "http://localhost:8000":
        print("Registration and Auto-Login Successful - PASSED")
        os.makedirs("evidence", exist_ok=True)
        driver.save_screenshot("evidence/evidence_login.png")
        
        # Save credentials for search, validation, and CRUD tests to use
        with open("test_credentials.txt", "w") as f:
            f.write(f"{test_email}\n{test_pass}")
    else:
        print("Registration Failed - FAILED")
        os.makedirs("evidence", exist_ok=True)
        driver.save_screenshot("evidence/evidence_login_failed.png")

finally:
    driver.quit()