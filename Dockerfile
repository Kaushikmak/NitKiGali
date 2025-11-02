# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code as the 'app' user
COPY --chown=app:app . .

# Collect static files
RUN python manage.py collectstatic --no-input

# Switch to the non-root user
USER app

# Expose the port Daphne will run on
EXPOSE 8000

# Run Daphne.
CMD daphne -b 0.0.0.0 -p $PORT nitkigali.asgi:application