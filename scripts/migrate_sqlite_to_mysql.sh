#!/usr/bin/env bash
# Run this script in a PythonAnywhere Bash console from the project root.
# Prerequisites:
#   1. Create your MySQL database in PythonAnywhere -> Databases tab.
#   2. Create ski/prod_settings.py (see ski/prod_settings.example.py).
#   3. Make sure your virtualenv is activated.

set -euo pipefail

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DB="backups/db.sqlite3.${TIMESTAMP}.bak"
DUMP_FILE="backups/prod_dump_${TIMESTAMP}.json"

mkdir -p backups

if [ ! -f "db.sqlite3" ]; then
    echo "Error: db.sqlite3 not found in $(pwd)"
    exit 1
fi

echo "1) Backing up db.sqlite3 -> ${BACKUP_DB}"
cp db.sqlite3 "${BACKUP_DB}"

echo "2) Exporting SQLite data -> ${DUMP_FILE}"
# Temporarily force DEBUG=True so settings.py reads from SQLite during dumpdata
DEBUG=True python manage.py dumpdata \
    --natural-foreign --natural-primary \
    -e contenttypes -e auth.Permission \
    --indent 2 -o "${DUMP_FILE}"

echo "3) Running migrations on MySQL (DEBUG=False)"
if [ ! -f "ski/prod_settings.py" ]; then
    echo "Error: ski/prod_settings.py not found. Copy ski/prod_settings.example.py and fill in your MySQL credentials."
    exit 1
fi

DEBUG=False python manage.py migrate

echo "4) Loading data into MySQL"
DEBUG=False python manage.py loaddata "${DUMP_FILE}"

echo "5) Verifying Order count in MySQL:"
DEBUG=False python manage.py shell -c "from apps.home.models import Order; print('Orders in MySQL:', Order.objects.count())"

echo "Done! Remember to set DEBUG=False in .env and reload your WebApp in PythonAnywhere."

