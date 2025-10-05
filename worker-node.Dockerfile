# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY worker_requirements.txt .
RUN pip install --no-cache-dir -r worker_requirements.txt

# Copy worker scripts
COPY worker.py .
COPY test_sample.py .

# Install pytest (for job execution)
RUN pip install pytest

# Command to run the worker node
CMD ["python", "worker.py"]

