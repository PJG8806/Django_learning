from .local import *

DEBUG = False

ALLOWED_HOSTS = ['kkugi.pythonanywhere.com'] # 배포할 주소

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# ln -sf prod.py settings.py  이 방식으로 환경 불리가 가능