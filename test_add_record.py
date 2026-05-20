from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import time
import random
import os

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

try:
    # 1. Open the public Artist Application form
    driver.get("http://127.0.0.1:8000/apply-artist/")
    time.sleep(2)
    
    # Generate randomized artist details
    random_id = random.randint(1000, 9999)
    artist_email = f"artist_{random_id}@example.com"
    artist_phone = f"0999{random.randint(1000000, 9999999)}"
    artist_name = f"Test Artist {random_id}"

    # 2. Fill out Applicant Information
    driver.find_element(By.NAME, "applicant_name").send_keys("Test Applicant")
    driver.find_element(By.NAME, "applicant_email").send_keys(artist_email)
    driver.find_element(By.NAME, "applicant_phone").send_keys(artist_phone)
    driver.find_element(By.NAME, "artist_name").send_keys(artist_name)
    driver.find_element(By.NAME, "artist_municipality").send_keys("Daraga")
    driver.find_element(By.NAME, "artist_brgy").send_keys("Bagumbayan")
    driver.find_element(By.NAME, "artist_zipcode").send_keys("4501")
    driver.find_element(By.NAME, "artist_description").send_keys("Automated test artist description.")

    # 3. Open Product Modal
    driver.find_element(By.CLASS_NAME, "apply-add-btn").click()
    time.sleep(1)
    
    # 4. Fill out product draft in the modal
    driver.find_element(By.ID, "draftName").send_keys("Test Artwork")
    driver.find_element(By.ID, "draftPrice").send_keys("150")
    driver.find_element(By.ID, "draftStock").send_keys("3")
    driver.find_element(By.ID, "draftNewCategory").send_keys("Sculptures")
    driver.find_element(By.ID, "draftDescription").send_keys("A beautiful automated test artwork.")
    
    # Save the draft product
    driver.find_element(By.CLASS_NAME, "modal-save-btn").click()
    time.sleep(1)

    # 5. Submit the application
    driver.find_element(By.CLASS_NAME, "apply-submit").click()
    time.sleep(3) # Wait for page reload/redirection

    # Verify that the database record was successfully added
    if "Your artist application has been submitted and is waiting for admin review." in driver.page_source:
        print("Record Added - PASSED")
        os.makedirs("evidence", exist_ok=True)
        driver.save_screenshot("evidence/evidence_crud.png")
    else:
        print("Record Not Added - FAILED")
        os.makedirs("evidence", exist_ok=True)
        driver.save_screenshot("evidence/evidence_crud_failed.png")

finally:
    driver.quit()