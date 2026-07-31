FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/src"

RUN apt-get update && apt-get install -y --no-install-recommends \
    p7zip-full \
    unzip \
    unrar-free \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml .
COPY src/ ./src/
COPY meowdfer.py .

RUN pip install --no-cache-dir .
RUN chmod +x meowdfer.py

# Absolute path guarantees execution regardless of container workdir
ENTRYPOINT ["python", "/app/meowdfer.py"]