#!/bin/sh

echo "⏳ Esperando base de datos..."
# Esperar que DB esté accesible, opcional:
# while ! nc -z $DB_HOST $DB_PORT; do sleep 1; done

echo "🚀 Aplicando migraciones..."
python manage.py migrate

echo "📦 Cargando datos (si backup existe)..."
if [ -f "backup.json" ]; then
  python manage.py loaddata backup.json
fi

echo "🌐 Iniciando servidor..."
exec uvicorn UpLife.asgi:application --host 0.0.0.0 --port 8000 --lifespan off
