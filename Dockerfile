# A2A Hub MVP image (Python 3.11+; 3.12 used for current slim base)
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    A2A_HUB_HOST=0.0.0.0 \
    A2A_HUB_PORT=8000 \
    A2A_HUB_DATABASE_PATH=/app/data/a2a_hub.db \
    A2A_HUB_LOG_LEVEL=INFO

WORKDIR /app

# Install package first for better layer caching when only app code changes later
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY config ./config
COPY samples ./samples
COPY scripts ./scripts

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir . \
    && mkdir -p /app/data

EXPOSE 8000

# Serve only — crawl is a separate one-shot command (ADR-008)
CMD ["python", "-m", "a2a_hub", "serve"]
