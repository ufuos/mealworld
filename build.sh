#!/usr/bin/env bash
set -euo pipefail
echo "Collect static files"
python manage.py collectstatic --noinput
echo "Apply database migrations"
python manage.py migrate --noinput
