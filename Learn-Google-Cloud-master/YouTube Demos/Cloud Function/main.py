from google.cloud import storage

# Define the destination bucket for invalid files
INVALID_FILES_BUCKET = "bkt-cfdemo-dest-000"

def check_file_size_and_move(event, context):
    """Triggered by a change to a GCS bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    source_bucket_name = event['bucket']
    file_name = event['name']

    # Initialize GCS client
    storage_client = storage.Client()
    source_bucket = storage_client.bucket(source_bucket_name)
    blob = source_bucket.blob(file_name)

    # Reload blob metadata to ensure size is fetched
    blob.reload()

    # Get file size in bytes
    file_size = blob.size

    # Ensure file size is not None
    if file_size is None:
        print(f"Unable to determine the size for {file_name}. Skipping.")
        return

    max_size = 2 * 1024 * 1024  # 2MB in bytes

    if file_size > max_size:
        # Move the file to the "large_files/" folder in the destination bucket
        destination_bucket = storage_client.bucket(INVALID_FILES_BUCKET)
        new_blob_name = f"large_files/{file_name}"  # Add folder prefix
        new_blob = source_bucket.copy_blob(blob, destination_bucket, new_blob_name)
           
        # Delete the original file
        blob.delete()

        print(f"File {file_name} moved to {INVALID_FILES_BUCKET}/large_files/{file_name} because it exceeds 2MB.")
    else:
        print(f"File {file_name} is within the size limit (<= 2MB). No action taken.")
