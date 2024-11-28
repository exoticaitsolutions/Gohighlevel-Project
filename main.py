import time
# from get_otp import login_gmail
from login_with_google_api import otp_get_from
from urls import *
from utils import status_check_folder_or_not
from webdriver_configration import driver_confrigration
import logging
from datetime import datetime
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the google_credentials path from the .env file
GOHIGHLEVEL_EMAIL = os.getenv('GOHIGHLEVEL_EMAIL')
GOHIGHLEVEL_PASSWORD = os.getenv('GOHIGHLEVEL_PASSWORD')
print("GOHIGHLEVEL_EMAIL : ", GOHIGHLEVEL_EMAIL)
print("GOHIGHLEVEL_PASSWORD : ", GOHIGHLEVEL_PASSWORD)



def setup_logging():
    # Create the logs_detail directory if it doesn't exist
    log_dir = "logs_detail"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Generate a log file name based on the current date
    log_file = os.path.join(log_dir, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")
    
    # Set up logging configuration
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,  # Set the logging level to INFO
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode='a'  # Append to the existing log file
    )
    logger = logging.getLogger()
    return logger

def scrapping():
    logger = setup_logging()
    logger.info("Starting the scrapping process.")
    
    try:
        driver = driver_confrigration()
        logger.info("Driver configuration completed.")
        
        driver.get(WEBSITE_URL)
        logger.info(f"Navigated to {WEBSITE_URL}.")
        time.sleep(20)
        
        email_box = driver.find_element(By.ID, 'email')
        email_box.send_keys(GOHIGHLEVEL_EMAIL)
        logger.info("Entered email.")
        
        password_box = driver.find_element(By.ID, 'password')
        password_box.send_keys(GOHIGHLEVEL_PASSWORD)
        logger.info("Entered password.")
        
        signup_button = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[4]/section/div[2]/div/div/div/div[4]/div/button')
        signup_button.click()
        logger.info("Clicked on signup button.")
        
        time.sleep(5)
        
        send_security_code = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[4]/section/div[2]/div/div/div/div[3]/div/button')
        send_security_code.click()
        logger.info("Sent security code.")
        
        time.sleep(45)
        logger.info("Waiting for OTP.")
        
        # Uncomment and integrate OTP processing as needed
        security_code = otp_get_from()
        time.sleep(10)
        otp_digits = list(str(security_code))
        otp_inputs = driver.find_elements(By.CLASS_NAME, 'otp-input')
        for i, digit in enumerate(otp_digits):
            otp_inputs[i].send_keys(digit)
        time.sleep(40)
        
        logger.info("Login successful.")
        
        automation_button = driver.find_element(By.ID, "sb_automation")
        automation_button.click()
        logger.info("Navigated to automation.")
        time.sleep(45)
        
        try:
            driver.switch_to.frame("workflow-builder")
            logger.info("Switched to iframe 'workflow-builder'.")
        except Exception as e:
            logger.error(f"Iframe not found: {e}")
        
        time.sleep(10)
        
        main_publish_list = status_check_folder_or_not(driver)
        logger.info(f"Publish list obtained: {main_publish_list}")
    
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
    
    logger.info("Scrapping process completed.")

# Call the function
scrapping()




