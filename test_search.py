from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import time
import os

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

try:
    # BicoLikha search is a public page and doesn't require login.
    # We will search for 'Matcha', which is one of the mock products in the SQL dump.
    driver.get("http://127.0.0.1:8000/search/?q=Matcha")
    time.sleep(2)
    
    # Verify the result is visible in the page source or a product container
    if "Matcha" in driver.page_source:
        print("Search Function - PASSED")
        os.makedirs("evidence", exist_ok=True)
        driver.save_screenshot("evidence/evidence_search.png")
    else:
        print("Search Function - FAILED")
        os.makedirs("evidence", exist_ok=True)
        driver.save_screenshot("evidence/evidence_search_failed.png")

finally:
    driver.quit()