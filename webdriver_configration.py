import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from selenium import webdriver


def driver_confrigration():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    
    # Use Service for ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    
    # Pass options and service to Chrome WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    return driver



# FOR DOCKER------------------------------------------------------------

# def driver_confrigration():
#     # Set Chrome options
#     print("333333333333333333333")
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--no-sandbox")
#     options.add_argument('--disable-gpu')
#     options.add_argument("--remote-debugging-port=9222") 
#     service = Service(executable_path="chromedriver-linux64/chromedriver")
#     driver = webdriver.Chrome(service=service, options=options)
#     driver.set_page_load_timeout(180)  # Set a longer timeout for page load
#     driver.set_script_timeout(180)  # Set a
    
#     return driver

