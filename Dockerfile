# Use the official Python image
FROM python:3.10-slim

# Install system dependencies and clean up to reduce image size
RUN apt-get update && apt-get install -y curl iputils-ping apt-utils && apt-get clean

# Set the working directory
WORKDIR /app

# Install dependencies for creating virtual environments
RUN python3 -m venv /opt/venv

# Ensure the virtual environment is used by default
ENV PATH="/opt/venv/bin:$PATH"

# Copy the requirements.txt first to leverage Docker caching
COPY requirements.txt .

# Install dependencies in the virtual environment
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port and set the entry point
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
