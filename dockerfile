# Use a slim Python image to keep the footprint small (Senior MLOps practice)
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed for some Python packages (like C compilers)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker's layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a directory for the local database to ensure persistence
RUN mkdir -p /app/local_db

# Expose the FastAPI port
EXPOSE 8000

# Run the application using uvicorn
CMD ["python", "-m", "src.serving.app"]