#!/usr/bin/env sh
set -e

# Default ports can be overridden from docker-compose.yml or `docker run -e`
: "${REDIS_HOST:=redis}"
: "${REDIS_PORT:=6379}"
: "${DB_HOST:=db}"
: "${DB_PORT:=5432}"

echo "⏳ Waiting for Redis @$REDIS_HOST:$REDIS_PORT..."
until nc -z "$REDIS_HOST" "$REDIS_PORT"; do
  sleep 1
done
echo "✅ Redis is up."

echo "⏳ Waiting for database @$DB_HOST:$DB_PORT..."
until nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done
echo "✅ Database is up."

echo "🔄 Running migrations..."
python manage.py migrate --noinput

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Start Celery worker in the background
echo "🚀 Starting Celery worker..."
celery -A djangoproject worker -l info &

# Optional: start Celery beat (uncomment if you use periodic tasks)
# echo "🚀 Starting Celery beat..."
# celery -A djangoproject beat -l info &

# Finally run the Django app (Gunicorn HTTP server)
echo "🚀 Starting Gunicorn..."
exec gunicorn djangoproject.wsgi:application --bind 0.0.0.0:8000
