#!/bin/bash

set -a
source .env
set +a

echo "Waiting for PostgreSQL to start..."
RETRY_COUNT=0
MAX_RETRIES=30
until nc -z postgres 5432 || [ $RETRY_COUNT -eq $MAX_RETRIES ]; do
  sleep 1
  RETRY_COUNT=$((RETRY_COUNT+1))
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
  echo "PostgreSQL did not start within the timeout limit."
  exit 1
fi

echo "PostgreSQL started!"

cd /usr/src/app/regx_backend

# Print for debugging before makemigrations
echo "Running makemigrations..."
python manage.py makemigrations --noinput
if [ $? -ne 0 ]; then
  echo "Error occurred during makemigrations"
  exit 1
fi

# Print for debugging before migrate
echo "Running migrations..."
python manage.py migrate --noinput
if [ $? -ne 0 ]; then
  echo "Error occurred during migrate"
  exit 1
fi

echo "Make migrations finished!"

# Print for debugging before starting server
echo "Starting the Django server..."
exec python manage.py runserver 0.0.0.0:8000

