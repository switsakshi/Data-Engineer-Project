import json
from datetime import datetime
from google.cloud import storage  # Google Cloud Storage client library

# Constants
BUCKET_NAME = "bkt-cloudrun-job-demo"  # Your bucket name


# Simulate database connection and fetching sales data
def fetch_sales_data():
    """Simulate fetching sales data from a database."""
    print("Fetching sales data...")
    # Simulate sales data
    sales_data = [
        {"product": "Laptop", "quantity": 5, "total_price": 5000},
        {"product": "Headphones", "quantity": 15, "total_price": 1500},
        {"product": "Smartphone", "quantity": 10, "total_price": 8000},
    ]
    return sales_data


# Generate a simple summary report
def generate_report(data):
    """Generate a sales summary report."""
    print("Generating sales report...")
    total_sales = sum(item["total_price"] for item in data)
    total_items = sum(item["quantity"] for item in data)
    report = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total_sales": total_sales,
        "total_items_sold": total_items,
        "details": data,
    }
    return report


# Save the report to Google Cloud Storage
def save_report_to_gcs(report, bucket_name):
    """Save the report to a GCS bucket."""
    print("Saving report to GCS...")
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Create a unique filename
    file_name = f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    # Save report as a JSON file
    blob = bucket.blob(file_name)
    blob.upload_from_string(json.dumps(report), content_type="application/json")

    print(f"Report saved to GCS: {file_name}")


# Main function
def main():
    """Fetch, process, and save the daily sales report."""
    try:
        sales_data = fetch_sales_data()
        report = generate_report(sales_data)

        save_report_to_gcs(report, BUCKET_NAME)
        print("Daily sales report generation completed successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
