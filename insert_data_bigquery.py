from datetime import datetime
from big_query_script import client
import os
from dotenv import load_dotenv
from utils import *

# Load environment variables from the .env file
load_dotenv()

project_id = os.getenv('bigquery_project_id')
dataset_id = os.getenv('bigquery_dataset_id')


def get_last_workflow_id():
    table_id = "workflow_actions"
    # This function should query your database to get the last inserted workflow_id.
    # This example assumes you're using a SQL database or BigQuery and it retrieves the highest ID.
    query = f"""
    SELECT MAX(workflow_id) FROM `{project_id}.{dataset_id}.{table_id}`
    """
    result = client.query(query).result()
    last_id = result[0][0] if result else 0  # If no rows, return 0
    return last_id


def insert_row_in_work_flow_actions(rows_to_insert):
    table_id = "workflow_actions"
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    
    # Get the last workflow_id and increment it by 1
    last_workflow_id = get_last_workflow_id()
    new_workflow_id = 1 if last_workflow_id == 0 else last_workflow_id + 1  # Start from 1 if no data
    
    # Update the rows with the new workflow_id
    for row in rows_to_insert:
        row["workflow_id"] = new_workflow_id  # Assign the incremented ID
        
        # Handle empty last_updated_date
        if not row["last_updated_date"]:  # Check if last_updated_date is empty or None
            row["last_updated_date"] = "DEFAULT_VALUE"  # You can replace with a default value like '2024-11-26'

    # Insert rows into the table
  
    errors = client.insert_rows_json(table_ref, rows_to_insert)  # API call
    if not errors:
        print("==============="*8)
        print("Data inserted successfully!")
        logger.info("Data inserted successfully workflow_actions table!")
        print("==============="*8)
    else:
        print(f"Encountered errors while inserting data: {errors}")


def insert_data_into_workflow_actions_stats(email_stats_data, sms_stats_data):
    table_id = "workflow_actions_stats"
    # Define the table 
    print("enetr function insert_data_into_workflow_actions_stats ")
    table_ref = f"{project_id}.{dataset_id}.workflow_actions_stats"

    # Fetch the current maximum workflow_action_id
    query = f"""
        SELECT MAX(workflow_action_id) AS max_id
        FROM `{table_ref}`
    """
    query_job = client.query(query)  # Execute the query
    max_id = None
    for row in query_job:
        max_id = row["max_id"]

    # Determine the next workflow_action_id
    next_id = (max_id + 1) if max_id is not None else 1  # Start from 1 if no records exist

    # Prepare the data to insert based on the table schema
    rows_to_insert = [
        {
            "workflow_action_id": next_id,  # Use the incremented ID
            "last_updated_date": email_stats_data.get("last_updated_date", "2024-11-25T12:00:00Z"),
            
            # SMS statistics
            "stats_sms_count_total": sms_stats_data.get("stats_sms_count_total", 0),
            "stats_sms_count_delivered": sms_stats_data.get("stats_sms_count_delivered", 0),
            "stats_sms_count_clicked": sms_stats_data.get("stats_sms_count_clicked", 0),
            "stats_sms_count_failed": sms_stats_data.get("stats_sms_count_failed", 0),
            "stats_sms_percent_delivered": sms_stats_data.get("stats_sms_percent_delivered", "0%"),
            "stats_sms_percent_clicked": sms_stats_data.get("stats_sms_percent_clicked", "0%"),
            "stats_sms_percent_failed": sms_stats_data.get("stats_sms_percent_failed", "0%"),
            
            # Email statistics
            "stats_email_count_total": email_stats_data.get("stats_email_count_total", 0),
            "stats_email_count_delivered": email_stats_data.get("stats_email_count_delivered", 0),
            "stats_email_count_opened": email_stats_data.get("stats_email_count_opened", 0),
            "stats_email_count_clicked": email_stats_data.get("stats_email_count_clicked", 0),
            "stats_email_count_replied": email_stats_data.get("stats_email_count_replied", 0),
            "stats_email_count_bounced": email_stats_data.get("stats_email_count_bounced", 0),
            "stats_email_count_unsubscribed": email_stats_data.get("stats_email_count_unsubscribed", 0),
            "stats_email_count_rejected": email_stats_data.get("stats_email_count_rejected", 0),
            "stats_email_count_complained": email_stats_data.get("stats_email_count_complained", 0),
            
            "stats_email_percent_delivered": email_stats_data.get("stats_email_percent_delivered", "0%"),
            "stats_email_percent_opened": email_stats_data.get("stats_email_percent_opened", "0%"),
            "stats_email_percent_clicked": email_stats_data.get("stats_email_percent_clicked", "0%"),
            "stats_email_percent_replied": email_stats_data.get("stats_email_percent_replied", "0%"),
            "stats_email_percent_bounced": email_stats_data.get("stats_email_percent_bounced", "0%"),
            "stats_email_percent_unsubscribed": email_stats_data.get("stats_email_percent_unsubscribed", "0%"),
            "stats_email_percent_rejected": email_stats_data.get("stats_email_percent_rejected", "0%"),
            "stats_email_percent_complained": email_stats_data.get("stats_email_percent_complained", "0%"),
        }
    ]

    # Insert rows into the table
    errors = client.insert_rows_json(table_ref, rows_to_insert)  # API call
    if not errors:
        print("Data inserted successfully!")
        logger.info("Data inserted successfully workflow_actions_stats table!")
    else:
        print(f"Encountered errors while inserting data: {errors}")
