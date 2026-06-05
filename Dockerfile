# Legacy stack: Django 1.11 on Python 3.6 (EOL). Pinned base image so the
# old dependency set resolves to wheels instead of failing to build on a
# modern host. Runs under amd64 emulation on Apple Silicon.
FROM python:3.6-slim-buster

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=settings_dev

WORKDIR /app/source

# Curated dependency set for *local dev*: original pins for the Django stack,
# but C-extension packages (Pillow) left to resolve to a cp36 wheel, and no
# psycopg2/boto3 since dev uses SQLite + local-disk storage. The full original
# pins live in source/requirements.txt for production parity.
RUN pip install --no-cache-dir \
        "Django==1.11.1" \
        "django-allauth==0.30.0" \
        "django-crispy-forms==1.6.1" \
        "django-storages==1.5.2" \
        "geoip2==2.9.0" \
        "Pillow==8.4.0" \
        "pytz==2021.3"

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
