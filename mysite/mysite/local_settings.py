import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure--obolfim_-s$i=gexofz#&4w8exx(qyz#7^+6w!9=)dcl12cqq'

DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'film',
        'USER': 'postgres',
        'PASSWORD': 'hp13199113',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

STATIC_URL = 'static/'
