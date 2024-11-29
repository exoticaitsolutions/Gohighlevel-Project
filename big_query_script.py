from google.cloud import bigquery
from google.oauth2 import service_account
import os
from google.oauth2 import service_account
from dotenv import load_dotenv
from utils import *


# Load environment variables from the .env file
load_dotenv()

# Access the google_credentials path from the .env file
google_credentials = os.getenv('google_credentials')
project_id = os.getenv('bigquery_project_id')
dataset_id = os.getenv('bigquery_dataset_id')


# Create the credentials object
credentials = service_account.Credentials.from_service_account_file(google_credentials)

# Load credentials from the service account file
credentials = service_account.Credentials.from_service_account_file(google_credentials)

# Initialize the BigQuery client with credentials
client = bigquery.Client(credentials=credentials, project=project_id)


def show_all_table_in_database():
    # Reference the dataset
    dataset_ref = client.dataset(dataset_id)

    # List all tables in the dataset
    print(f"Tables in dataset '{dataset_id}':")
    tables = client.list_tables(dataset_ref)  # API call
    for table in tables:
        print(table.table_id)

# Define the table schema

def crate_table_workflow_actions():
    table_id = "workflow_actions"
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    schema = [
        bigquery.SchemaField("workflow_id", "INTEGER", mode="REQUIRED", description="Unique ID for each category"),
        bigquery.SchemaField("name", "STRING", mode="REQUIRED", description="Name of the category"),
        bigquery.SchemaField("step", "INTEGER", mode="REQUIRED", description="Step number in workflow"),
        bigquery.SchemaField("type", "STRING", mode="REQUIRED", description="Email, SMS, etc."),
        bigquery.SchemaField("last_updated_date", "TIMESTAMP", mode="REQUIRED", description="Last updated timestamp"),
    ]

    # Check if the table already exists
    try:
        client.get_table(table_ref)  # API call to fetch table details
        print(f"Table '{table_id}' already exists in dataset '{dataset_id}'.")
        logger.info(f"Table '{table_id}' already exists in dataset '{dataset_id}'.")
    except Exception as e:
        if "Not found" in str(e):
            # Create the table if it doesn't exist
            table = bigquery.Table(table_ref, schema=schema)
            client.create_table(table)  # API call
            print(f"Table '{table_id}' created successfully in dataset '{dataset_id}'.")
            logger.info(f"Table '{table_id}' created successfully in dataset '{dataset_id}'.")
        else:
            print(f"Table '{table_id}' already created in dataset '{dataset_id}'.")

# crate_table_workflow_actions()


def create_table_for_workflow_action_stats():
    table_id = "workflow_actions_stats"

    # Load credentials from the service account file
    credentials = service_account.Credentials.from_service_account_file(google_credentials)

    # Initialize the BigQuery client with credentials
    client = bigquery.Client(credentials=credentials, project=project_id)

    # Step 1: Define the table schema
    schema = [
        bigquery.SchemaField("workflow_action_id", "INTEGER", mode="REQUIRED", description="Unique ID for each workflow action"),
        bigquery.SchemaField("last_updated_date", "TIMESTAMP", mode="REQUIRED", description="Last updated timestamp"),

        bigquery.SchemaField("stats_sms_count_total", "INTEGER", mode="REQUIRED", description="Total SMS count"),
        bigquery.SchemaField("stats_sms_count_delivered", "INTEGER", mode="REQUIRED", description="Delivered SMS count"),
        bigquery.SchemaField("stats_sms_count_clicked", "INTEGER", mode="REQUIRED", description="Clicked SMS count"),
        bigquery.SchemaField("stats_sms_count_failed", "INTEGER", mode="REQUIRED", description="Failed SMS count"),
        bigquery.SchemaField("stats_sms_percent_delivered", "STRING", mode="REQUIRED", description="Delivered percentage of SMS"),
        bigquery.SchemaField("stats_sms_percent_clicked", "STRING", mode="REQUIRED", description="Clicked percentage of SMS"),
        bigquery.SchemaField("stats_sms_percent_failed", "STRING", mode="REQUIRED", description="Failed percentage of SMS"),

        bigquery.SchemaField("stats_email_count_total", "INTEGER", mode="REQUIRED", description="Total email count"),
        bigquery.SchemaField("stats_email_count_delivered", "INTEGER", mode="REQUIRED", description="Delivered email count"),
        bigquery.SchemaField("stats_email_count_opened", "INTEGER", mode="REQUIRED", description="Opened email count"),
        bigquery.SchemaField("stats_email_count_clicked", "INTEGER", mode="REQUIRED", description="Clicked email count"),
        bigquery.SchemaField("stats_email_count_replied", "INTEGER", mode="REQUIRED", description="Replied email count"),
        bigquery.SchemaField("stats_email_count_bounced", "INTEGER", mode="REQUIRED", description="Bounced email count"),
        bigquery.SchemaField("stats_email_count_unsubscribed", "INTEGER", mode="REQUIRED", description="Unsubscribed email count"),
        bigquery.SchemaField("stats_email_count_rejected", "INTEGER", mode="REQUIRED", description="Rejected email count"),
        bigquery.SchemaField("stats_email_count_complained", "INTEGER", mode="REQUIRED", description="Complained email count"),

        bigquery.SchemaField("stats_email_percent_delivered", "STRING", mode="REQUIRED", description="Delivered percentage of emails"),
        bigquery.SchemaField("stats_email_percent_opened", "STRING", mode="REQUIRED", description="Opened percentage of emails"),
        bigquery.SchemaField("stats_email_percent_clicked", "STRING", mode="REQUIRED", description="Clicked percentage of emails"),
        bigquery.SchemaField("stats_email_percent_replied", "STRING", mode="REQUIRED", description="Replied percentage of emails"),
        bigquery.SchemaField("stats_email_percent_bounced", "STRING", mode="REQUIRED", description="Bounced percentage of emails"),
        bigquery.SchemaField("stats_email_percent_unsubscribed", "STRING", mode="REQUIRED", description="Unsubscribed percentage of emails"),
        bigquery.SchemaField("stats_email_percent_rejected", "STRING", mode="REQUIRED", description="Rejected percentage of emails"),
        bigquery.SchemaField("stats_email_percent_complained", "STRING", mode="REQUIRED", description="Complained percentage of emails"),
    ]

    # Define the table reference
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    # Check if the table already exists
    try:
        client.get_table(table_ref)
        print(f"Table '{table_id}' already exists in dataset '{dataset_id}'.")
        logger.info(f"Table '{table_id}' already exists in dataset '{dataset_id}'.")
    except Exception as e:
        if "Not found" in str(e):
            # Create the table if it doesn't exist
            table = bigquery.Table(table_ref, schema=schema)
            table = client.create_table(table)  # API call
            print(f"Table '{table_id}' created successfully in dataset '{dataset_id}'.")
            logger.info(f"Table '{table_id}' created successfully in dataset '{dataset_id}'.")
        else:
            raise  

# create_table_for_workflow_action_stats()
        

def show_data_in_workflow_action_stats():
    table_id = "workflow_actions_stats"
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    
    # Query to fetch all data from the table
    query = f"""
    SELECT *
    FROM `{table_ref}`
    """
    
    # Run the query
    query_job = client.query(query)  # API call to execute the query
    
    # Fetch and display the results
    rows = query_job.result()
    print(f"Data in table '{table_id}':")
    for row in rows:
        print(dict(row))  # Convert each row to a dictionary for better readability

    query = f"""
        SELECT MAX(workflow_action_id) AS max_id
        FROM `{table_ref}`
    """
    query_job = client.query(query)  # Execute the query
    max_id = None
    for row in query_job:
        max_id = row["max_id"]

    # Determine the next workflow_action_id
    next_id = (max_id + 1) if max_id is not None else 1
    print("next_id : -----------", next_id)

# show_data_in_workflow_action_stats()


def  show_data_for_actions_table():
    table_id = "workflow_actions"
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    # Query to fetch all data from the table
    query = f"""
    SELECT *
    FROM `{table_ref}`
    """

    # Run the query
    query_job = client.query(query)  # API call to execute the query

    # Fetch the results
    rows = query_job.result()

    # Print the results
    print(f"Data from table '{table_id}':")
    for row in rows:
        print(dict(row))  # Convert Row object to a dictionary for better readability

# show_data_for_actions_table()
