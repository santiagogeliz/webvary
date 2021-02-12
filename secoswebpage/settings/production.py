from .base import *
import os
import dj_database_url
from decouple import config, Csv

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)


# STATIC & MEDIA
# ------------------------
MEDIA_ROOT = '/home/webvary/media_webvary/'
MEDIA_URL = '/media/'


# EMAIL
# ------------------------------------------------------------------------------
EMAIL_HOST = config('EMAIL_HOST'),
EMAIL_HOST_USER = config('EMAIL_HOST_USER'),
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD'),
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL'),
SERVER_EMAIL = config('SERVER_EMAIL'),
