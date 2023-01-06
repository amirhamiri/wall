from .base import *


DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


STATIC_URL = 'static/'
STATIC_ROOT = '/home/static'
MEDIA_URL = 'media/'
MEDIA_ROOT = '/home/media'