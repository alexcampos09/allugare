"""Local development / demo settings for allugare.

Self-contained settings used to run the project locally (e.g. for portfolio
screenshots or a client demo) WITHOUT the production AWS/S3 + Heroku Postgres
stack.

It lives as a TOP-LEVEL module (next to manage.py) on purpose: the
``allugare.settings`` package's ``__init__.py`` eagerly runs
``from .base import *`` / ``from .production import *``, which fail because
those modules reference files absent from this repo (``allugare.aws.conf``,
``allugare.utils`` storage classes) and email secrets commented out in
``passwords.py``. Importing anything *under* that package triggers the broken
chain, so we sidestep it entirely.

Run with::

    DJANGO_SETTINGS_MODULE=settings_dev

Differences from production:
  * SQLite instead of Postgres (zero-config; no psycopg2 build needed).
  * Static/media served from local disk instead of S3.
  * Console email backend (no real SMTP).
  * DEBUG on, ALLOWED_HOSTS open.

To point this at Postgres for a real client, set the ``DATABASE_URL`` env var
(see the commented dj_database_url block below) or replace ``DATABASES``.
"""

import os

# This module sits at source/ (the Django project root, next to manage.py).
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dev-only key. We can't import allugare.settings.passwords here because that
# triggers the broken settings-package __init__ chain (see module docstring).
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-insecure-key-change-me")

DEBUG = True
ALLOWED_HOSTS = ["*"]

GEOIP_PATH = os.path.join(BASE_DIR, "geoip")

# --- Email: print to console, never reach out to SMTP in local dev ---
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_MAIN = "viva@allugare.com.br"
DEFAULT_FROM_EMAIL = "viva@allugare.com.br"

# --- Applications (mirrors production.py, minus the S3/email coupling) ---
INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # The login/signup templates reference the facebook provider directly, so
    # it must be installed AND have a SocialApp row (seed_demo creates a dummy
    # one) or the pages 500. The button is visual-only without real FB creds.
    "allauth.socialaccount.providers.facebook",
    "crispy_forms",
    "storages",
    # project apps
    "analytics",
    "landing",
    "lares",
    "mensagens",
    "profiles",
)

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

# --- django-allauth ---
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
ACCOUNT_ADAPTER = "profiles.adapter.AccountAdapter"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "allugare.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "templates/account"),
            os.path.join(BASE_DIR, "templates/blog"),
            os.path.join(BASE_DIR, "templates/error"),
            os.path.join(BASE_DIR, "templates/land"),
            os.path.join(BASE_DIR, "templates/lares"),
            os.path.join(BASE_DIR, "templates/mensagens"),
            os.path.join(BASE_DIR, "templates/profiles"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "allugare.wsgi.application"

# --- Database: SQLite by default. Set DATABASE_URL to use Postgres instead. ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
# To run against Postgres (e.g. for a real client), install dj-database-url +
# psycopg2 and uncomment:
# import dj_database_url
# if os.environ.get("DATABASE_URL"):
#     DATABASES["default"] = dj_database_url.config(conn_max_age=500)

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# --- Static & media from local disk (NOT S3) ---
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static-live", "static")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "static-live", "media")

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

CRISPY_TEMPLATE_PACK = "bootstrap3"

SOCIALACCOUNT_PROVIDERS = {
    "facebook": {
        "METHOD": "js_sdk",
        "SCOPE": ["email", "public_profile"],
        "FIELDS": ["id", "email", "name", "first_name", "last_name"],
        "VERSION": "v2.4",
    }
}
