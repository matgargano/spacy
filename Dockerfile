# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install numpy first to avoid binary incompatibility
RUN pip install --no-cache-dir numpy==1.21.6

# Install the rest of the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download the spaCy English model
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application code
COPY . .

# Expose port 5001 for the Flask app
EXPOSE 5001

# Set the command to run the Flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
