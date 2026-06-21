#!/usr/bin/env bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKUP_DIR="$PROJECT_DIR/backups"
DATE=$(date +%Y-%m-%d_%H-%M-%S)

mkdir -p "$BACKUP_DIR"

DB_FILE="$PROJECT_DIR/db.sqlite3"
if [ -f "$DB_FILE" ]; then
  cp "$DB_FILE" "$BACKUP_DIR/db_$DATE.sqlite3"
  gzip "$BACKUP_DIR/db_$DATE.sqlite3"
  echo "SQLite backup created: $BACKUP_DIR/db_$DATE.sqlite3.gz"
fi

find "$BACKUP_DIR" -name "*.gz" -mtime +14 -delete

echo "Backup finished at $DATE"
