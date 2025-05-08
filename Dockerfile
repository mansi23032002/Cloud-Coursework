# Use the official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY req.txt .
RUN pip install --upgrade pip && pip install -r req.txt

# Copy the app files
COPY . .

# Expose port
EXPOSE 8080

# Run the Flask app
CMD ["python", "main.py"]
