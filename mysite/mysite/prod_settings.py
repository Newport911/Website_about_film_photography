import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure--obolfim_-s$i=gexofzgdfg#&4w8e9-9xx(qyz#7^+gdfg6w!9=)dcl12cqq'

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']


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

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')