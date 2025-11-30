# 가계부 백엔드 (Django + uv)

Django REST Framework 기반 가계부 애플리케이션 백엔드입니다.

## 🚀 빠른 시작

### 1. uv로 실행 (권장)

```bash
# 백엔드 디렉토리로 이동
cd backend

# 개발 서버 실행 (자동으로 의존성 설치 및 마이그레이션)
./dev.sh
```

또는 프로젝트 루트에서:

```bash
./run-backend.sh
```

### 2. 직접 실행

```bash
cd backend

# 의존성 설치 (최초 1회만)
uv sync

# 마이그레이션 (최초 1회만)
uv run python manage.py migrate

# 개발 서버 실행
uv run python manage.py runserver
```

## 📦 주요 의존성

- Django 5.2.1
- Django REST Framework 3.16.0
- django-cors-headers (CORS 지원)
- django-filter (필터링)
- drf-spectacular (API 문서)
- psycopg2-binary (PostgreSQL)

## 🔧 환경 설정

`.env` 파일을 생성하고 필요한 환경변수를 설정하세요:

```bash
# .env.example을 복사
cp .env.example .env

# 필요한 값 설정
SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=household_budget.settings.dev
```

## 📚 API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- Swagger UI: http://localhost:8000/api/docs/
- OpenAPI Schema: http://localhost:8000/api/schema/

## 🛠️ 유용한 명령어

```bash
# 관리자 계정 생성
uv run python manage.py createsuperuser

# Django 셸 실행
uv run python manage.py shell

# 새 마이그레이션 생성
uv run python manage.py makemigrations

# 마이그레이션 적용
uv run python manage.py migrate

# 테스트 실행
uv run python manage.py test

# 정적 파일 수집 (운영 환경)
uv run python manage.py collectstatic
```

## 📂 프로젝트 구조

```
backend/
├── apps/
│   ├── accounts/      # 사용자 인증
│   ├── categories/    # 카테고리 관리
│   ├── transactions/  # 거래 관리
│   └── assets/        # 자산 관리
├── household_budget/
│   ├── settings/      # 환경별 설정
│   └── urls.py
├── middleware/        # 커스텀 미들웨어
├── pyproject.toml     # uv 프로젝트 설정
├── .python-version    # Python 버전
└── manage.py
```

## 🌍 환경별 실행

### 개발 환경 (기본)
```bash
uv run python manage.py runserver
```

### 운영 환경
```bash
export DJANGO_SETTINGS_MODULE=household_budget.settings.prod
uv run python manage.py runserver
```

## 📝 참고사항

- Python 3.10 이상 필요
- uv가 자동으로 Python 3.10을 설치합니다
- 개발 환경에서는 SQLite3 사용
- 운영 환경에서는 PostgreSQL 사용
