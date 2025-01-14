# Project Name
## Gohighlevel-Project

# Setup Instructions

## Installation

### Python Installation Process
Before proceeding, ensure Python is installed on your system. If not, you can download and install Python from [python.org](https://www.python.org/downloads/).

### Setting up a Virtual Environment
To work with Django, it's recommended to create a virtual environment. Follow the steps outlined in the [Python documentation](https://docs.python.org/3/tutorial/venv.html) or use tools like `virtualenv` or `venv`.

## Getting Started

### Clone the Project
```bash
git clone https://github.com/exoticaitsolutions/GoHighLvel-Docker.git
```

## Navigate to the Project Directory

```bash
  cd GoHighLvel-Docker
```

# Install Dependencies
### Using requirements.txt
```
pip install -r requirements.txt
```

# Individual Dependencies

***Selenium***
```
pip install selenium
```

***Webdriver Manager***
```
pip install webdriver-manager
```

## Setup .env File
Place the ghl-data-warehouse-437615-f27cdafe5d38.json file in the root directory of your project.
```
google_credentials = "ghl-data-warehouse-437615-f27cdafe5d38.json"
```

# Creating a Table for a New JSON in BigQuery
* If you want to create a table for a new JSON file, uncomment the create_table_workflow_actions() function in the bigquery_script.py file.
## Steps to Follow:
```
1. Open the bigquery_script.py file in your project.
2. Locate the crate_table_workflow_actions() and create_table_for_workflow_action_stats function.
3. Uncomment the function call in the script.
4. Run the bigquery_script to create the table in BigQuery.
```

# Verifying Data Insertion in the Table
* To check if the data has been successfully inserted into the table, uncomment the show_data_in_workflow_actions() function in the bigquery_script.py file.
## Steps to Follow:
```
1. Open the bigquery_script.py file in your project.
2. Locate the show_data_in_workflow_action_stats() and show_data_for_actions_table() function.
3. Uncomment the function call in the script.
4. Run the bigquery_script to display the data from the table.
```

# Run Project
```bash
python main.py
```

# Docker Setup
* Follow this documentation for setup in your system 
https://docs.google.com/document/d/1qwG3WvPFFUCOsp3oLpv5owO6k2PPBptTaa6kJLnZqlE/edit?tab=t.0

# Running the Application with Docker
## 1. Build the Docker Image
Run the following command to build the Docker image and tag it as python-app:
```
docker build -t python-app .
```

# Run the Docker Container
``
docker run -it --name my-python-container --shm-size=4g --memory=8g --cpus="4" python-app
``
# Stop the Container
To stop the running container, execute:
```
docker stop my-python-container
```

# Remove the Container
Once the container is stopped, you can remove it with:
```
docker rm my-python-container
```
# Gohighlevel-Project
# Gohighlevel-Project
