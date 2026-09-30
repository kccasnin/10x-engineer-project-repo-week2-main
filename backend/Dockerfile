# Use an appropriate, lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Set environment variables to optimize Python running in a container
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy the requirements file first to leverage Docker's layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY app ./app
COPY main.py .

# Expose the port the application runs on
EXPOSE 8000

# Set the default command to run the application
# Note: docker-compose.yml overrides this to add --reload for development
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]