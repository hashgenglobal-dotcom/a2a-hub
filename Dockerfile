# A2A Hub MVP image (Python 3.11+; 3.12 used for current slim base)
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    A2A_HUB_HOST=0.0.0.0 \
    A2A_HUB_DATABASE_PATH=/app/data/a2a_hub.db \
    A2A_HUB_LOG_LEVEL=INFO

WORKDIR /app

# Install package first for better layer caching when only app code changes later
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY config ./config
COPY samples ./samples
COPY scripts ./scripts
COPY entrypoint.sh ./entrypoint.sh

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir . \
    && mkdir -p /app/data \
    && chmod +x /app/entrypoint.sh

EXPOSE 8000

# Entrypoint: crawl on first boot, then serve
CMD ["/app/entrypoint.sh"]
