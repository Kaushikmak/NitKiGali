# Use official Python image
FROM python:3.12-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Make start script executable
COPY start.sh .
RUN chmod +x start.sh

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port for local testing
EXPOSE 8000

# Start using the script
CMD ["./start.sh"]