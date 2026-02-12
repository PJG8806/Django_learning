from pathlib import Path
import os
from dotenv import load_dotenv
from corsheaders.defaults import default_headers

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
    'corsheaders',  # CORS 헤더 앱 서로 다른 서버에서 실행 된 부분 또는 주소가 다른 경우 처리
    'users.apps.UsersConfig',  # 커스텀 사용자 앱
    'posts.apps.PostsConfig',  # 게시물 앱
    'comments.apps.CommentsConfig',  # 댓글 앱
]

MIDDLEWARE = [
    # CORS 설정을 위한 미들웨어 추가 (베스트 프랙티스)
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",

    # 기본 미들웨어
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

# CORS 설정 (베스트 프랙티스)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",        # 로컬 프론트 개발
    "https://app.example.com",      # 운영 프론트
]

# 추가적인 헤더 허용 설정 jwt 토큰 처리를 위해 사용할 일은 거의 없다
CORS_ALLOW_HEADERS = list(default_headers) + [
    "authorization",
    "x-csrftoken",
]

# 프론트에서 접근 가능한 헤더 설정 노출 헤더
CORS_EXPOSE_HEADERS = [
    "content-disposition",
]

# CSRF, 쿠키, SameSite 신뢰할 수 있는 출처 설정
CSRF_TRUSTED_ORIGINS = [
    "https://app.example.com",
]

# 프론트에서 fetch(..., { credentials: "include" }) 또는 axios withCredentials: true 쓰면,
CORS_ALLOW_CREDENTIALS = True  # 쿠키, 인증 헤더 등 자격 증명 허용 

# SameSite 설정 None으로 해야 크로스 도메인에서 쿠키 전달 됨
SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# 프론트에서 필수로 해야 하는 거
# 프론트에서 자격 증명 포함 요청 예시 
# fetch("https://api.example.com/v1/...", {
#   method: "POST",
#   credentials: "include",
#   headers: { "Content-Type": "application/json" },
#   body: JSON.stringify(data),
# });
# axios.post("https://api.example.com/v1/...", data, {
#   withCredentials: true,
# });

# Nginx 프록시 붙이면 안될수도 있다
# 404/502면 Nginx 설정에서 proxy_set_header  부분 확인 필요
# 아니면 크로스 오리진 막힌거일수도 있다 이러면 장고로 다이렉트로 붙여서 접속이 된다면 Preflight(OPTIONS) 요청이 막힌거다 옵션을 허용해줘야 한다

# CORS 문제 해결 체크리스트
# - [ ]  프론트 Origin과 API Origin을 정확히 파악했다(스키마/호스트/포트).
# - [ ]  `corsheaders`가 `INSTALLED_APPS`에 들어갔다.
# - [ ]  `CorsMiddleware`가 `CommonMiddleware`보다 위에 있다.
# - [ ]  운영에서 `CORS_ALLOWED_ORIGINS`로 명시 허용(무분별한 `ALLOW_ALL` 금지).
# - [ ]  쿠키/세션이면 `CORS_ALLOW_CREDENTIALS=True` + 프론트 credentials 옵션을 켰다.
# - [ ]  쿠키/세션이면 `CSRF_TRUSTED_ORIGINS`를 적절히 설정했다.
# - [ ]  필요한 경우 SameSite/Secure 설정으로 쿠키 전달 문제를 해결했다(HTTPS 전제).
# - [ ]  Network 탭에서 Preflight(OPTIONS)와 실제 요청의 응답 헤더를 확인했다.
# - [ ]  “Django 응답인지 / 프록시 응답인지”를 구분했다(에러 응답일수록 중요).