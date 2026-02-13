from .base import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

STATIC_URL = 'static/'
STATIC_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / '.static_root'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': SECRET['DB']['NAME'],
        'USER': SECRET['DB']['USER'],
        'PASSWORD': SECRET['DB']['PASSWORD'],
        'HOST': SECRET['DB']['HOST'],
        'PORT': SECRET['DB']['PORT'],
    }
}