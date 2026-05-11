# Use Python 3.11 slim Bullseye image as base
FROM python:3.11-slim-bullseye

# Set environment variables
# Prevents Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1
# Disable pip version check for faster install
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies for Python package builds
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libssl-dev \
    libffi-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt
COPY requirements.txt /app/

# Upgrade pip and install dependencies
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY backend/ /app/

# Expose port 8000
EXPOSE 8000

# Run Django development server
# For production, replace with: gunicorn backend.wsgi:application --bind 0.0.0.0:8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
