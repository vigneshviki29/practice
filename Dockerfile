# Use a lightweight official Python image
FROM python:3.11-slim

# Set the operational directory inside the container
WORKDIR /app

# Copy the dependency tracking file first to leverage cache
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual application files into the image
COPY app.py .

# Expose port 5000 so the host network can map to it
EXPOSE 5000

# Start up the web server when the container starts
CMD ["python", "app.py"]
