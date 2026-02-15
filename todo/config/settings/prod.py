from .base import *

DEBUG = True

ALLOWED_HOSTS = ['13.125.168.60',
                 'localhost']

# Static
STATIC_URL = 'static/'
STATIC_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / '.static_root'

# Media
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# DB
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}
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


ROOT_URLCONF = "config.urls"
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'sconfig.storage_backends.MediaStorage'
