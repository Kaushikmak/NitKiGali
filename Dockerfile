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

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port for local testing
EXPOSE 8000

# Start Daphne with dynamic Railway port (or fallback to 8000)
CMD ["sh", "-c", "daphne -b 0.0.0.0 -p ${PORT:-8000} nitkigali.asgi:application"]