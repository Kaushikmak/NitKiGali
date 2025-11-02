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

# Collect static files (optional)
RUN python manage.py collectstatic --noinput || true

# Expose the default port
EXPOSE 8000

# Default port fallback (in case $PORT not set)
ENV PORT=8000

# Run Daphne directly
CMD ["sh", "-c", "daphne -b 0.0.0.0 -p $PORT nitkigali.asgi:application"]
