from google.cloud import pubsub_v1
import json

# Replace with your GCP project ID and Pub/Sub topic name
project_id = "tt-dev-001"
topic_id = "dfdemo"

# Publisher client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Message to send
message = {
    "empid": 101,
    "name": "John Doe",
    "salary": 75000
}

# Convert the message to a JSON string
message_json = json.dumps(message).encode("utf-8")

# Publish the message
future = publisher.publish(topic_path, message_json)

# Print the message ID
print(f"Message published with ID: {future.result()}")
