# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY apiserver_requirements.txt .
RUN pip install --no-cache-dir -r apiserver_requirements.txt

# Copy FastAPI server code
COPY fastapi-server.py .

# Expose FastAPI's port
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "fastapi-server:app", "--host", "0.0.0.0", "--port", "8000"]

