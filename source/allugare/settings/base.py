"""
Django settings for allugare project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
from .passwords import SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

EMAIL_HOST = 'smtp.gmail.com'
from .passwords import EMAIL_HOST_USER
from .passwords import EMAIL_HOST_PASSWORD
EMAIL_MAIN = 'contato@placehunters.com.br'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

""" If using gmail, you will need to unlock Captcha to enable Django
to send for you: https://accounts.google.com/displayunlockcaptcha """


# Application definition

INSTALLED_APPS = (
    #DJANGO APPS
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #THIRD PARTY APPS
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

         #Social Authentications
        'allauth.socialaccount.providers.facebook',
        # 'allauth.socialaccount.providers.instagram',
        # 'allauth.socialaccount.providers.twitter',

    'crispy_forms',
    'django_messages',
    'storages',

    #MY APPS
    'lares',
    'mensagens',
    'profiles',
)

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# DJANGO ALLAUTH SETTINGS
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# AllAuth redirect to username view
ACCOUNT_ADAPTER = 'profiles.adapter.AccountAdapter'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware', Django 1.8
]

ROOT_URLCONF = 'allugare.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates/account'),
            os.path.join(BASE_DIR, 'templates/blog'),
            os.path.join(BASE_DIR, 'templates/error'),
            os.path.join(BASE_DIR, 'templates/profiles'),
            os.path.join(BASE_DIR, 'templates/lares'),
            os.path.join(BASE_DIR, 'templates/mensagens'),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                #THIRD PARTY APPS
                'django_messages.context_processors.inbox',
            ],
        },
    },
]

WSGI_APPLICATION = 'allugare.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_allugare',
        'USER': 'alexcampos',
        'PASSWORD': 'incorrect',
        'HOST': 'localhost',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'
# LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "static_root")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    )

MEDIA_URL = '/media/'
MEDIA_ROOT =  os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "media_root")

AWS_ACCESS_KEY_ID = "AKIAIRMGKN5UTHCW2ZAQ"
AWS_SECRET_ACCESS_KEY = "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"


AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True

DEFAULT_FILE_STORAGE = 'allugare.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'allugare.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 's3allugare'
S3DIRECT_REGION = 'sa-east-1'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
os.environ['S3_USE_SIGV4'] = 'True'
AWS_S3_HOST = 'sa-east-1.amazonaws.com'

import datetime

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = {
	'Expires': expires,
	'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}




# CRISPY FORM TAGs SETTINGS
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# http://localhost:8000/accounts/facebook/login/callback/
SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
       {'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time'],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'pt_BR',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.4'
        }
    }
