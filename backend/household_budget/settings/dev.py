# backend/house_budget/settings/dev.py

from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# 개발용 SQLite DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CORS 설정
CORS_ALLOWED_ORIGINS = [
    "http://localhost:9000",  # Quasar 개발 서버
    "http://127.0.0.1:9000",  # 대안 주소
]

# 개발 환경에서만 모든 도메인 허용 (선택사항)
CORS_ALLOW_ALL_ORIGINS = True  # 개발 시에만 사용, 운영에서는 False

# 허용할 HTTP 메서드
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# 허용할 헤더
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# 개발용 이메일, 캐시 등 필요시 추가
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'