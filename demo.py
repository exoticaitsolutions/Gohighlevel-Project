import csv
import time
# from get_otp import login_gmail
from login_with_google_api import otp_get_from
from urls import *
# from webdriver_configration import driver_confrigration
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
    
GOHIGHLEVEL_EMAIL = 'webbdeveloper24@gmail.com'
GOHIGHLEVEL_PASSWORD = 'Exotica@123#'
def driver_confrigration():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    
    # Use Service for ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    
    # Pass options and service to Chrome WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scraping():
    print("---"*20)
    driver = driver_confrigration()
    print("-------driver-----")

    driver.get(WEBSITE_URL)
    time.sleep(20)
    email_box = driver.find_element(By.ID, 'email')
    email_box.send_keys(GOHIGHLEVEL_EMAIL)
    password_box = driver.find_element(By.ID, 'password')
    password_box.send_keys(GOHIGHLEVEL_PASSWORD)
    signup_button = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[4]/section/div[2]/div/div/div/div[4]/div/button')
    signup_button.click()
    time.sleep(5)
    send_security_code = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[4]/section/div[2]/div/div/div/div[3]/div/button')
    send_security_code.click()
    time.sleep(45)
    security_code = otp_get_from()
    time.sleep(10)
    otp_digits = list(str(security_code))
    otp_inputs = driver.find_elements(By.CLASS_NAME, 'otp-input')
    for i, digit in enumerate(otp_digits):
        otp_inputs[i].send_keys(digit)
    time.sleep(60)
        
    print("login successfully ----------")
    # driver.get(AUTOMATION_URL1)
    driver.get("https://app.gohighlevel.com/location/dazhY1JW8Bwxtehw16he/workflow/aeb6e6aa-e08c-41f9-ad76-cba88082a7ac")
    time.sleep(45)
    print("WORKFLOW_URL successfully ----------")
     # Refresh the current URL
    current_url = driver.current_url
    print(f"Refreshed current URL: {current_url}")
    driver.get(current_url)
    time.sleep(35)
    driver.switch_to.frame('workflow-builder')
    time.sleep(6)

    # Scrape workflow name
    scrap_name = driver.find_element(By.CSS_SELECTOR, 'h1[aria-label="Workflow Name"]')
    print("Workflow Name:", scrap_name.text)

    zoom_out_button = driver.find_element(By.ID, "workflow-zoom-out")
    for _ in range(13):
        zoom_out_button.click()
        time.sleep(1)
    print("ho gya zoom==================")

   
    print("-----"*8)

  
   
    # main_publish_list = status_check_folder_or_not(driver)
    print()
    print()
    print("Final publish list ")
    print(main_publish_list)
   

scraping()


