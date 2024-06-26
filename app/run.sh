#!/bin/sh

export APP_MODULE=${APP_MODULE:-app.main:app}
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8008}

# Применение миграций к базе данных
alembic upgrade head

exec uvicorn --reload --host $HOST --port $PORT "$APP_MODULE"