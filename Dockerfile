# Minimal Dockerfile for the Flask app
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (if needed for pandas/scikit-learn wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r /app/requirements.txt

# Copy application files
COPY . /app

# Expose port (Render will provide PORT env var)
ENV PORT=5000
EXPOSE $PORT

# Run with gunicorn
CMD ["gunicorn", "main:app", "-b", "0.0.0.0:$PORT", "--workers", "1"]
