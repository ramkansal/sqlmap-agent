FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    sqlmap \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Install Python dependencies
RUN pip install .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV SQLMAP_TIMEOUT_S=900
ENV LLM_MODEL=gpt-5-nano

# Default command
CMD ["python3", "main.py"]
