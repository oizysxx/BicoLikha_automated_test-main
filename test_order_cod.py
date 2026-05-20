from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import time
import os
import random

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

try:
    # 1. Retrieve credentials from the signup/login test if available
    username = "test_user@example.com"
    password = "Password123"
    
    if os.path.exists("test_credentials.txt"):
        with open("test_credentials.txt", "r") as f:
            lines = f.read().splitlines()
            if len(lines) >= 2:
                username = lines[0]
                password = lines[1]
                print(f"Loaded credentials from test_credentials.txt: {username}")

    # 2. Login to customer portal
    driver.get("http://127.0.0.1:8000/accounts/login/")
    time.sleep(2)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    # 3. Navigate to a seeded product detail page (e.g. prod_id=112)
    driver.get("http://127.0.0.1:8000/product/112/")
    time.sleep(2)

    # Click the "Buy Now" button
    try:
        driver.find_element(By.CSS_SELECTOR, ".btn-buy-now").click()
    except Exception as e:
        print(f"DEBUG: Failed to click Buy Now. Current URL: {driver.current_url}")
        print(f"DEBUG: Page source snippet: {driver.page_source[:1000]}")
        os.makedirs("evidence", exist_ok=True)
        driver.save_screenshot("evidence/evidence_order_cod_debug.png")
        raise e
    time.sleep(2)

    # 4. Check if we need to add a delivery address
    if "No delivery address yet" in driver.page_source or len(driver.find_elements(By.NAME, "add_new_address")) > 0:
        print("Address not found or new address modal detected. Adding a delivery address...")
        
        # Open the address modal if it isn't already open
        if len(driver.find_elements(By.NAME, "st_name")) == 0 or not driver.find_element(By.NAME, "st_name").is_displayed():
            driver.find_element(By.XPATH, "//button[contains(text(), 'ADD NEW ADDRESS')]").click()
            time.sleep(1)
        
        # Fill out the address modal form
        driver.find_element(By.NAME, "st_name").send_keys("123 Automated Street")
        driver.find_element(By.NAME, "brgy").send_keys("San Jose")
        driver.find_element(By.NAME, "municipality").send_keys("Legazpi City")
        driver.find_element(By.NAME, "zipcode").send_keys("4500")
        
        phone_num = f"0917{random.randint(1000000, 9999999)}"
        driver.find_element(By.NAME, "phone").send_keys(phone_num)
        
        # Save Address
        driver.find_element(By.NAME, "add_new_address").click()
        time.sleep(2)

    # 5. Place the Order (COD is selected by default)
    # Click the main checkout place order button
    driver.find_element(By.CSS_SELECTOR, ".btn-place-order").click()
    time.sleep(1)

    # Confirm checkout in the confirmation modal
    driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm & Place Order')]").click()
    time.sleep(4) # Wait for processing

    # 6. Verify successful placement
    if "Order Placed Successfully!" in driver.page_source:
        print("Order Placement via COD - PASSED")
        os.makedirs("evidence", exist_ok=True)
        driver.save_screenshot("evidence/evidence_order_cod.png")
    else:
        print("Order Placement via COD - FAILED")
        os.makedirs("evidence", exist_ok=True)
        driver.save_screenshot("evidence/evidence_order_cod_failed.png")


finally:
    driver.quit()
