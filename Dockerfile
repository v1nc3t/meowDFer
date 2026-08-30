FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Archive backends required by patoolib
RUN apt-get update && apt-get install -y --no-install-recommends \
    p7zip-full \
    unzip \
    unrar-free \
    xz-utils \
    tar \
    gzip \
    bzip2 \
    file \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src/ ./src/

RUN pip install --no-cache-dir .

ENTRYPOINT ["meowdfer"]
