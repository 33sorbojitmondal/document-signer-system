#!/bin/bash
set -e
pip install -r requirements.txt
python manage.py collectstatic --noinput
if [ -n "$DATABASE_URL" ]; then
  python manage.py migrate --noinput
  python manage.py create_authority
fi
