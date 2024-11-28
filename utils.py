import os
import re
import time
from datetime import datetime
import logging
from insert_data_bigquery import insert_data_into_workflow_actions_stats, insert_row_in_work_flow_actions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def process_email(driver):
    logger = setup_logging()
    logger.info("Starting the scrapping process process email ")
    email_actions = driver.find_elements(By.XPATH, '//*[@aria-label="Email Action"]')
    print("email_actions length: ", len(email_actions))

    for i in range(len(email_actions)):
        print("------------------email---------------------------------------------------------------------")
        print("=" * 18)
        print("Processing email", i + 1, "of", len(email_actions))
        logger.info(f"Processing email {i + 1} of {len(email_actions)}")

        # Refresh the list of email actions
        email_actions = driver.find_elements(By.XPATH, '//*[@aria-label="Email Action"]')
        email = email_actions[i]  # Get the current email action
        email.click()
        time.sleep(8)

        # Process email stats
        stats = driver.find_element(By.XPATH, '//*[@id="cmp-email-act__tab--stats"]')
        stats.click()
        time.sleep(3)

        details = driver.find_element(By.XPATH, '//div[@id="cmp-email-stats__link--details-delivered"]/a')
        details.click()
        time.sleep(5)

        email_stats_data = {
            # "workflow_action_id": i + 1,  # Or dynamically fetch ID
            "last_updated_date": "2024-11-25T12:00:00Z",  # Example timestamp

            "stats_email_count_total": driver.find_element(By.ID, "cmp-stat-modal__btn--stat-card-total").text,

            "stats_email_percent_delivered": driver.find_element(By.ID, "cmp-stat-modal__btn--stat-card-delivered").text,
            "stats_email_count_delivered": driver.find_element(By.XPATH, '//*[@id="main"]/section/div/div/div[1]/div[2]/div/fieldset/div/div[2]/div[3]/div/div/div[2]/div/div[3]/label').text,
           
            "stats_email_percent_clicked": driver.find_element(By.ID, "cmp-stat-modal__btn--stat-card-clicked").text,
            "stats_email_count_clicked": driver.find_element(By.XPATH, '//*[@id="main"]/section/div/div/div[1]/div[2]/div/fieldset/div/div[2]/div[3]/div/div/div[2]/div/div[3]/label').text,

            "stats_email_percent_opened": driver.find_element(By.ID, "cmp-stat-modal__btn--stat-card-opened").text,
            "stats_email_count_opened": driver.find_element(By.XPATH, '//*[@id="main"]/section/div/div/div[1]/div[2]/div/fieldset/div/div[2]/div[3]/div/div/div[2]/div/div[3]/label').text,

            "stats_email_percent_replied": driver.find_element(By.ID, "cmp-stat-modal__btn--stat-card-replied").text,
            "stats_email_count_replied": driver.find_element(By.XPATH, '//*[@id="main"]/section/div/div/div[1]/div[2]/div/fieldset/div/div[2]/div[3]/div/div/div[2]/div/div[3]/label').text,

            "stats_email_percent_bounced": driver.find_element(By.ID, "cmp-stat-modal__btn--stat-card-permanent_fail").text,
            "stats_email_count_bounced": driver.find_element(By.XPATH, '//*[@id="main"]/section/div/div/div[1]/div[2]/div/fieldset/div/div[2]/div[3]/div/div/div[2]/div/div[3]/label').text,

            "stats_email_percent_unsubscribed": driver.find_element(By.ID, "cmp-stat-modal__btn--stat-card-unsubscribed").text,
            "stats_email_count_unsubscribed": driver.find_element(By.XPATH, '//*[@id="main"]/section/div/div/div[1]/div[2]/div/fieldset/div/div[2]/div[3]/div/div/div[2]/div/div[3]/label').text,

            "stats_email_percent_rejected":"",
            "stats_email_count_rejected":"",

            "stats_email_percent_complained":"",
            "stats_email_count_complained":"",
        }
        print("email_stats_data : ", email_stats_data)
        logger.info(f"email_stats_data : {email_stats_data}")

        def clean_and_convert(value):
            if isinstance(value, str):
                # Extract digits using regex
                match = re.search(r'\d+', value)
                return int(match.group()) if match else 0
            return value

        # Apply cleaning to specific fields
        fields_to_clean = [key for key in email_stats_data if 'count' in key or 'percent' in key]

        for field in fields_to_clean:
            email_stats_data[field] = clean_and_convert(email_stats_data[field])

        print("email_stats_data cleaned : ", email_stats_data)
        logger.info(f"email_stats_data cleaned : {email_stats_data}")

        # Close the details view
        driver.find_element(By.XPATH, '//*[@id="main"]/section/div/div/div[1]/div[2]/div/fieldset/div/div[2]/div[3]/div/div/div[2]/div/div[1]/span').click()
        driver.find_element(By.XPATH, '//*[@id="cancel-button-aside-section"]/span').click()
        time.sleep(5)
    return email_stats_data


def process_sms(driver):
    logger = setup_logging()
    logger.info("Starting the scrapping process process sms ")
   
    sms_actions = driver.find_elements(By.XPATH, '//*[@aria-label="SMS Action"]')
    print("sms_actions length: ", len(sms_actions))
    logger.info(f"sms actions length: {len(sms_actions)}")


    for i in range(len(sms_actions)):
        print("------------------sms---------------------------------------------------------------------")
        print("=" * 18)
        print("Processing sms", i + 1, "of", len(sms_actions))
        logger.info(f"Processing sms {i + 1} of {len(sms_actions)}")

        # Refresh the list of SMS actions
        sms_actions = driver.find_elements(By.XPATH, '//*[@aria-label="SMS Action"]')
        sms = sms_actions[i]
        sms.click()
        time.sleep(5)

        # Process SMS stats
        stats = driver.find_element(By.ID, 'cmp-sms-act__tab--stats')
        stats.click()

        details = driver.find_element(By.ID, 'cmp-sms-stats__link--details-delivered')
        details.click()
        time.sleep(5)

        sms_stats_data = {
            "stats_sms_count_total": driver.find_element(By.ID, "cmp-stat-modal__btn--stat-card-total").text,

            "stats_sms_percent_delivered": driver.find_element(By.ID, "cmp-stat-modal__btn--stat-card-delivered").text,
            "stats_sms_count_delivered": driver.find_element(By.XPATH, '//*[@id="main"]/section/div/div/div[1]/div[2]/div/fieldset/form/div[2]/div[2]/div/div/div[2]/div/div[3]/label').text,

            "stats_sms_percent_clicked": driver.find_element(By.ID, "cmp-stat-modal__btn--stat-card-clicked").text,
            "stats_sms_count_clicked": driver.find_element(By.XPATH, '//*[@id="main"]/section/div/div/div[1]/div[2]/div/fieldset/form/div[2]/div[2]/div/div/div[2]/div/div[3]/label').text,

            "stats_sms_percent_failed": driver.find_element(By.ID, "cmp-stat-modal__btn--stat-card-failed").text,
            "stats_sms_count_failed": driver.find_element(By.XPATH, '//*[@id="main"]/section/div/div/div[1]/div[2]/div/fieldset/form/div[2]/div[2]/div/div/div[2]/div/div[3]/label').text
        }
        print()
        print()
        print("Sms Stats data:", sms_stats_data)
        logger.info(f"Sms Stats data: {sms_stats_data}")
        
        def clean_and_convert(value):
            if isinstance(value, str):
                # Extract digits using regex
                match = re.search(r'\d+', value)
                return int(match.group()) if match else 0
            return value

        # Apply cleaning to specific fields
        fields_to_clean = [key for key in sms_stats_data if 'count' in key or 'percent' in key]

        for field in fields_to_clean:
            sms_stats_data[field] = clean_and_convert(sms_stats_data[field])

        print("Sms Stats data cleaned :", sms_stats_data)
        logger.info(f"Sms Stats data cleaned :{sms_stats_data}")
        
        # insert_data_into_workflow_actions_stats(sms_stats_data)

        print()
        print()
    
        # Close the details view
        driver.find_element(By.XPATH, '//*[@id="main"]/section/div/div/div[1]/div[2]/div/fieldset/form/div[2]/div[2]/div/div/div[2]/div/div[1]/span').click()
        driver.find_element(By.XPATH, '//*[@id="cancel-button-aside-section"]/span').click()
        time.sleep(7)
    return sms_stats_data


def scrapp_email_sms(driver, url):
    logger = setup_logging()
    logger.info("scrapp_email_sms")
    action_type = ''
    print("url : ", url)
    driver.get(url)
    time.sleep(50)
    current_url = driver.current_url
    driver.get(current_url)
    time.sleep(35)

    # Switch to the correct iframe
    driver.switch_to.frame('workflow-builder')
    time.sleep(6)
    scrap_name = driver.find_element(By.CSS_SELECTOR, 'h1[aria-label="Workflow Name"]')
    logger.info(f"workfow diagram scrap name :{scrap_name.text}")
    print("workfow diagram scrap name : ", scrap_name.text)
    
    # Click on the all data section
    zoom_out_button = driver.find_element(By.ID, "workflow-zoom-out")
    print("zoom_out_button ----------------------------------------")
    for _ in range(13):
        zoom_out_button.click()
        time.sleep(1)
    print("ho gya zoom")
    all_data = driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/div/div[4]/div[1]/div[2]')
    all_data.click()
    time.sleep(4)
    email = driver.find_elements(By.XPATH, '//*[@aria-label="Email Notification to dedicated OS Action"]')
    sms = driver.find_elements(By.XPATH, '//*[@aria-label="SMS Action"]')
    logger.info(f"Email actions found: {len(email)}, SMS actions found: {len(sms)}")

    # If no email elements found, check for alternate email locator
    if not email:
        logger.info("No 'Email Notification to dedicated OS Action' found. Searching for 'Email Action'.")
        email = driver.find_elements(By.XPATH, '//*[@aria-label="Email Action"]')
        logger.info(f"Alternate email actions found: {len(email)}")

    # Process based on conditions
    if email and sms:
        logger.info("Both email and SMS actions found. Processing both.")
        email_stats_data = process_email(driver)
        sms_stats_data = process_sms(driver)
        action_type = "email & sms"
    elif email:
        logger.info("Only email actions found. Processing email.")
        email_stats_data = process_email(driver)
        sms_stats_data = None
        action_type = 'email'
    elif sms:
        logger.info("Only SMS actions found. Processing SMS.")
        email_stats_data = None
        sms_stats_data = process_sms(driver)
        action_type = 'sms'
    else:
        logger.info("No email or SMS actions found. Navigating to the next item.")
        print("No actions found. Skipping to the next.")
        email_stats_data = None
        sms_stats_data = None
        action_type = 'None'

    # Insert data into workflow actions stats if any actions were processed
    if email_stats_data or sms_stats_data:
        logger.info("Inserting processed data into workflow actions stats.")
        insert_data_into_workflow_actions_stats(email_stats_data, sms_stats_data)
    else:
        logger.info("No data to insert.")

    logger.info("scrapp_email_sms completed.")
    return action_type



def click_on_folder_or_file(driver,row):
    clicked_name = row.find_element(By.XPATH, ".//div[contains(@class, 'group-hover:text-primary-600') and contains(@class, 'cursor-pointer') and contains(@class, 'hl-text-sm-medium')]")
    print("clicked_name : ", clicked_name.text)
    clicked_name.click()
    time.sleep(5)
    click_url = driver.current_url 
    return click_url


main_publish_list = []
main_folder_list = []

def status_check_folder_or_not(driver):
    logger = setup_logging()
    logger.info("Check folder or not.")
  
    try:
        tbody = driver.find_element(By.CLASS_NAME, 'n-data-table-tbody')
        if tbody:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.6);")
            time.sleep(7)  # Allow time for the page to load
            icon_arrow = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//i[contains(@class, "n-base-icon n-base-suffix__arrow")]'))
                )
                # Click the icon
            icon_arrow.click()
            time.sleep(5)
            option = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//div[contains(@class, "n-base-select-option__content") and text()="50 / page"]')
                    )
                )
                # Click the option
            option.click()
            time.sleep(5)
        rows = tbody.find_elements(By.CLASS_NAME, 'n-data-table-tr')
        logger.info(f"Number of Rows Found: {len(rows)}")
        print("Number of Rows Found : ", len(rows))
        
    
        for i in  range(0,len(rows)):
            
            current_url = driver.current_url                                
            # Get the name cell value
            tbody = driver.find_element(By.CLASS_NAME, 'n-data-table-tbody')
        
            rows = tbody.find_elements(By.CLASS_NAME, 'n-data-table-tr')
            name_cell = rows[i].find_element(By.XPATH, './td[2]')
            updated_date = rows[i].find_element(By.XPATH, './td[5]')
            logger.info(f"updated_date: {updated_date.text}")
            
            print("updated_date : ", updated_date.text)

            if name_cell.text == 'Published':
                print("Entered Condition if  Published")
                logger.info(f"publish row updated_date: {updated_date.text}")
                logger.info(f"name of publish row: {name_cell.text}")
                print("name of publish row : ", name_cell.text)

                click_url  =  click_on_folder_or_file(driver,rows[i])

                main_publish_list.append(click_url)
                print("main_publish_list : ", main_publish_list)

                action_type = scrapp_email_sms(driver, click_url)

                rows_to_insert = [
                    {
                        "workflow_id": 0,  # Placeholder value that will be replaced with the incremented ID
                        "name": name_cell.text,
                        "step": 1,
                        "type": action_type,
                        "last_updated_date": updated_date.text or "2024-11-26",  # Default date if empty
                    },
                ]
                print("rows_to_insert : ", rows_to_insert)
                logger.info(f"rows_to_insert: {rows_to_insert}")

                insert_row_in_work_flow_actions(rows_to_insert)


                print("insert_row_in_work_flow_actions : -------------------"*88)
                driver.get(current_url)
                time.sleep(35)
                driver.switch_to.frame("workflow-builder")

            elif name_cell.text == "Draft":
                print("Entered Condition elif  Draft")
                logger.info("Entered Condition elif  Draft")
                logger.info(f"name of publish Draft : {name_cell.text}")

            else:
                print("Entered Condition else not Draft not publish its folder")
                logger.info("Entered Condition else not Draft not publish its folder")
                logger.info(f"name of Folder : {name_cell.text}")
                click_url =  click_on_folder_or_file(driver,rows[i])
                main_folder_list.append(click_url)
                driver.get(current_url)
                time.sleep(35)
                driver.switch_to.frame("workflow-builder")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")  # Log the error message
        print("here ---------------------------------------")
        print(f"An error occurred: {str(e)}")
    print("main_publish_list",main_publish_list)
    
    if len(main_folder_list) >=1:

        new_url = main_folder_list[0]
        driver.get(new_url)
        time.sleep(35)
        driver.switch_to.frame("workflow-builder")
        main_folder_list.pop(0)
        status_check_folder_or_not(driver)
    
    print()
    print("main_publish_list",main_publish_list)
    return main_publish_list