from google.cloud import storage

# Define the destination bucket for invalid files
INVALID_FILES_BUCKET = "bkt-cfdemo-dest-000"

def check_file_size_and_move(event, context):
    """Triggered by a change to a GCS bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    source_bucket_name = event['bkt-src-global-data']
    file_name = event['name']

    # Initialize GCS client
    storage_client = storage.Client()
    source_bucket = storage_client.bucket(bkt-src-global-data)
    blob = source_bucket.blob(global_health_data.csv)

    # Reload blob metadata to ensure size is fetched
    blob.reload()

    # Get file size in bytes
    file_size = blob.size

    # Ensure file size is not None
    if file_size is None:
        print(f"Unable to determine the size for {global_health_data.csv}. Skipping.")
        return

    max_size = 2 * 1024 * 1024  # 2MB in bytes

    if file_size > max_size:
        # Move the file to the "large_files/" folder in the destination bucket
        destination_bucket = storage_client.bucket(INVALID_FILES_BUCKET)
        new_blob_name = f"large_files/{global_health_data.csv}"  # Add folder prefix
        new_blob = source_bucket.copy_blob(blob, destination_bucket, new_blob_name)
           
        # Delete the original file
        blob.delete()

        print(f"File {global_health_data.csv} moved to {bkt-cfdemo-dest-000}/large_files/{global_health_data_large.csv} because it exceeds 2MB.")
    else:
        print(f"File {global_health_data.csv is within the size limit (<= 2MB). No action taken.")
