#!/bin/sh
# A2A Hub entrypoint — runs crawl on first boot, then starts the server.
# The crawl is skipped if the database already has resources (survives restart).

set -e

if [ ! -f "$A2A_HUB_DATABASE_PATH" ]; then
    echo "No database found. Running initial crawl..."
    python -m a2a_hub crawl || true
    echo "Crawl completed."
else
    echo "Database exists. Skipping initial crawl."
fi

echo "Starting server..."
exec python -m a2a_hub serve
