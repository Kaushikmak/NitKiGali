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

# Expose port - Railway will detect this
EXPOSE 8000

# Start Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "nitkigali.asgi:application"]