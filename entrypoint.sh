#!/bin/sh
# A2A Hub entrypoint — runs crawl if the database is empty, then starts the server.
# Uses a resource count check so an empty DB file doesn't block the initial crawl.

set -e

if [ -f "$A2A_HUB_DATABASE_PATH" ]; then
    # Check if the database actually has resources
    RESOURCE_COUNT=$(python -c "
import sqlite3, os
try:
    conn = sqlite3.connect(os.environ['A2A_HUB_DATABASE_PATH'])
    count = conn.execute('SELECT COUNT(*) FROM resources').fetchone()[0]
    conn.close()
    print(count)
except Exception:
    print('0')
" 2>/dev/null || echo "0")
else
    RESOURCE_COUNT="0"
fi

if [ "$RESOURCE_COUNT" = "0" ]; then
    echo "No resources found. Running initial crawl..."
    python -m a2a_hub crawl || true
    echo "Crawl completed."
else
    echo "Database has $RESOURCE_COUNT resources. Skipping initial crawl."
fi

echo "Starting server..."
exec python -m a2a_hub serve
