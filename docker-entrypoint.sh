#!/usr/bin/env bash
# Prepare the local dev database, then hand off to the container CMD.
set -e

echo "==> Applying migrations"
python manage.py migrate --noinput

echo "==> Seeding demo data (admin/admin + sample listings)"
python manage.py seed_demo

exec "$@"
