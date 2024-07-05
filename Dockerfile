# Use the official Python image from the Docker Hub based on Alpine Linux
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /app

# Install build dependencies and create a virtual environment
RUN apk add --no-cache gcc musl-dev libffi-dev

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Command to run the application using Gunicorn with Uvicorn workers
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:80"]
