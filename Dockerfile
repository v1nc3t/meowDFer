FROM python:3.12-slim

# Prevent Python from writing .pyc files & buffering stdout/stderr (vital for Docker logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies required by patoolib for extraction
RUN apt-get update && apt-get install -y --no-install-recommends \
    p7zip-full \
    unzip \
    unrar-free \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the modern configuration file first to leverage Docker build cache layers
COPY pyproject.toml .

# Install dependencies directly from the pyproject.toml file
RUN pip install --no-cache-dir .

# Copy the rest of the project source tree
COPY . .

# Make the wrapper executable
RUN chmod +x meowdfer.py

ENTRYPOINT ["python", "meowdfer.py"]