import os
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from webdriver_configration import driver_confrigration
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the google_credentials path from the .env file
email = os.getenv('email')
password = os.getenv('password')

def login_gmail():
    driver = driver_confrigration()
    print("---------- Start ------")

    try:
        driver.get("https://mail.google.com/")

        time.sleep(10)

        try:
            sign_in_button = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/header/div/div[4]/a[2]')
            if sign_in_button:
                sign_in_button.click()
        except:
            print("no sign in button found")

        
        email_field = driver.find_element(By.XPATH, '//*[@aria-label="Email or phone"]')
        email_field.send_keys(email)

       
        time.sleep(10)

        next = driver.find_element(By.ID, "identifierNext")
        next.click()
        print("email sucesssully submit")


        time.sleep(59)

        password_field = driver.find_element(By.XPATH, '//*[@aria-label="Enter your password"]')
        password_field.send_keys(password)
        time.sleep(10)
       
        next = driver.find_element(By.ID, "passwordNext")
        next.click()
        print("password_field sucesssully submit")


        print("Login successful!")

        time.sleep(35)

        topmsg= driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[8]/div/div[1]/div[2]/div/table/tbody/tr[1]/td[5]/div/div/span')
        msg = topmsg.text

        print("==========================>>>>>", msg)
        
        security_code = msg.split("code:")[1].split()[0]

        print("Security Code:", security_code)
        driver.quit()
        return security_code
     

    except (NoSuchElementException, TimeoutException) as e:
        print(f"An error occurred: {e}")
        driver.quit()
        return None