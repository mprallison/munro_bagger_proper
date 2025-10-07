# Use official Python runtime
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 8080

# Run the app with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]