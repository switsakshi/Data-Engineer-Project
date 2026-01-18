# Use Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy application code
COPY main.py /app/

# Install dependencies
RUN pip install --no-cache-dir google-cloud-storage

# Set the command to execute the Python script
CMD ["python3", "main.py"]
