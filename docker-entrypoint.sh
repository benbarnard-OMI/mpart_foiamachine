#!/bin/bash
set -e

echo "Waiting for database..."
# Simple wait using psql if available, otherwise skip
# Docker Compose healthchecks will ensure DB is ready before web starts
if command -v psql > /dev/null 2>&1 && [ -z "${SKIP_DB_CHECK:-}" ]; then
  DB_HOST=${DB_HOST:-db}
  DB_PORT=${DB_PORT:-5432}
  DB_NAME=${POSTGRES_DB:-foiamachine}
  DB_USER=${POSTGRES_USER:-foiamachine}
  DB_PASS=${POSTGRES_PASSWORD:-foiamachine_password}
  
  # Wait for PostgreSQL to be ready (max 30 seconds)
  COUNTER=0
  until PGPASSWORD="$DB_PASS" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c '\q' 2>/dev/null || [ $COUNTER -eq 30 ]; do
    >&2 echo "PostgreSQL is unavailable - sleeping ($COUNTER/30)"
    sleep 1
    COUNTER=$((COUNTER+1))
  done
  
  if [ $COUNTER -lt 30 ]; then
    echo "Database is ready!"
  else
    echo "Warning: Database check timed out, proceeding anyway..."
  fi
else
  echo "Skipping database check (psql not available or SKIP_DB_CHECK set)"
fi

# Set Django settings module
export DJANGO_SETTINGS_MODULE=foiamachine.config.settings

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || true

# Create superuser if it doesn't exist (optional, can be done manually)
# Uncomment the following lines if you want automatic superuser creation
# echo "Creating superuser if needed..."
# python manage.py shell << EOF
# from django.contrib.auth import get_user_model
# User = get_user_model()
# if not User.objects.filter(is_superuser=True).exists():
#     User.objects.create_superuser('admin', 'admin@example.com', 'admin')
# EOF

echo "Starting application..."
exec "$@"
