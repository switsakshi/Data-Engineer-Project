import csv
import time
from google.cloud import pubsub_v1
import json
from datetime import datetime

# Replace with your GCP project ID and Pub/Sub topic name
project_id = "tt-dev-02"
topic_id = "df-straming-demo"

# Pub/Sub Publisher Client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Function to publish a message to Pub/Sub
def publish_message(empid, firstname, salary):
    timestamp = datetime.utcnow().isoformat() + "Z"  # Add current UTC timestamp
    message = {
        "empid": empid,
        "name": firstname,
        "salary": salary,
        "timestamp": timestamp,
    }
    # Convert the message to JSON and encode as bytes
    message_json = json.dumps(message).encode("utf-8")
    # Publish the message
    publish_status = publisher.publish(topic_path, message_json)
    print(f"Published message with ID: {publish_status.result()} - {message}")

# Path to your CSV file
csv_file_path = "employee_data.csv"

# Publish records one by one
with open(csv_file_path, mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        empid = row["EmployeeID"]
        firstname = row["FirstName"]
        salary = row["Salary"]
        # Publish the record
        publish_message(empid, firstname, salary)
        # Wait for 30 seconds before publishing the next record
        time.sleep(5)  # Adjusted time to 30 seconds
