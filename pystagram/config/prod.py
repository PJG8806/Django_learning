from .base import *

DEBUG = False

ALLOWED_HOSTS = ['aws의 퍼블릭 주소 또는 도메인 주소']

INSTALLED_APPS += ['storages']
# 설정후 터미널 ls -sf local.py settings.py 입력 설정한 settings.py는 업로드 안하게 하고 서버에서 다시 입력으로 설정 해준다

DATABASES = {
    'default':{
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': SECRET['db']['name'],
    'USER': SECRET['db']['user'],
    'PASSWORD': SECRET['db']['password'],
    'HOST': SECRET['db']['host'],
    'port': '5432'
    }
}

AWS_ACCESS_KEY_ID = SECRET['S3']['key']
AWS_SECRET_ACCESS_KEY = SECRET['S3']['secret']
AWS_STORAGE_BUCKET_NAME = SECRET['S3']['name']

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'sconfig.storage_backends.MediaStorage'
