from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()  # .env 로드

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # DRF 추가
    'users.apps.UsersConfig',  # 커스텀 사용자 앱
    'posts.apps.PostsConfig',  # 게시물 앱
    'comments.apps.CommentsConfig',  # 댓글 앱
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'ko-KR'
TIME_ZONE = 'Asia/Seoul' # aws 별도 처리 안하면 시간 처리를 해야 한다

USE_I18N = True #internationalization
USE_TZ = True # timezone

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DRF 설정 (베스트 프랙티스: 기본 인증과 권한 설정)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ], # 세션 추가
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    # 익명 사용자와 인증된 사용자에 대한 기본 속도 제한 설정
    'DEFAULT_THROTTLE_CLASSES': [ 
        'rest_framework.throttling.AnonRateThrottle',# 로그인 안한 사용자 옵션
        'rest_framework.throttling.UserRateThrottle',# 로그인 한 사용자 옵션
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day', # 비회원은 하루에 100번
        'user': '1000/day',# 회원은 하루에 1000번
    },
}

# 커스텀 사용자 모델 (초기 설정 베스트 프랙티스)
AUTH_USER_MODEL = 'users.CustomUser' # django 기본 authentication, authorization
