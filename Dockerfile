# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies for creating virtual environments
RUN python3 -m venv /opt/venv

# Ensure the virtual environment is used by default
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install dependencies in the virtual environment
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port and set the entry point
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
