# Use official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose the port your app runs on
EXPOSE 8000

# Run the app
CMD ["python", "app.py"]
