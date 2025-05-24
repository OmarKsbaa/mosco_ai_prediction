# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies and Python packages in one layer to reduce image size
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn==0.24.0 \
    numpy==1.23.4 \
    joblib==1.3.2 \
    pydantic==2.5.2 \
    scikit-learn==1.2.2 \
    python-multipart==0.0.6 \
    httpx==0.25.2 \
    python-dotenv==1.0.0 \
    tensorflow-cpu==2.12.0 \
    h5py==3.8.0 \
    keras==2.12.0

# Copy the application
COPY app.py .
COPY Moscowregion.pkl .
COPY model2.keras .
COPY static static/

# Create non-root user
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port 8000
EXPOSE 8000

# Command to run the application with production settings
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--limit-concurrency", "100"]
