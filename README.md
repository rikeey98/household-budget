# 가계부 (Household Budget)

Django(백엔드) + Quasar(프론트엔드) 기반 가계부 프로젝트. Monorepo 구조로 전체 관리.

## 🚀 빠른 시작

### 필수 요구사항

- **백엔드**: uv (자동으로 Python 3.10 설치)
- **프론트엔드**: Node.js 16+

### 1️⃣ 백엔드 실행

```bash
./run-backend.sh
```

또는:

```bash
cd backend
./dev.sh
```

백엔드 서버: http://localhost:8000
API 문서: http://localhost:8000/api/docs/

### 2️⃣ 프론트엔드 실행

새 터미널에서:

```bash
./run-frontend.sh
```

또는:

```bash
cd frontend/quasar-project
npm install  # 최초 1회만
npm run dev
```

프론트엔드 서버: http://localhost:9000

## 📦 기술 스택

### 백엔드
- Django 5.2.1
- Django REST Framework 3.16.0
- Python 3.10+ (uv로 자동 관리)
- SQLite3 (개발) / PostgreSQL (운영)

### 프론트엔드
- Vue 3.4
- Quasar Framework 2.16
- Pinia (상태 관리)
- Axios (HTTP 클라이언트)

## 📂 프로젝트 구조

```
/
├── backend/              # Django 백엔드
│   ├── apps/
│   │   ├── accounts/     # 사용자 인증
│   │   ├── categories/   # 카테고리 관리
│   │   ├── transactions/ # 거래 관리
│   │   └── assets/       # 자산 관리
│   ├── pyproject.toml    # uv 프로젝트 설정
│   ├── .python-version   # Python 버전
│   └── dev.sh            # 개발 서버 실행 스크립트
├── frontend/             # Quasar 프론트엔드
│   └── quasar-project/
│       ├── src/
│       │   ├── pages/    # 페이지 컴포넌트
│       │   ├── stores/   # Pinia 스토어
│       │   └── services/ # API 클라이언트
│       └── package.json
├── run-backend.sh        # 백엔드 실행 스크립트
└── run-frontend.sh       # 프론트엔드 실행 스크립트
```

## ✨ 주요 기능

- ✅ 사용자 인증 (회원가입/로그인/로그아웃)
- ✅ 계층적 카테고리 관리 (대분류/소분류)
- ✅ 거래 내역 관리 (수입/지출)
- ✅ 고급 필터링 (날짜, 금액, 카테고리, 결제수단)
- ✅ 주간 요약 통계
- ⏳ 자산 관리 (개발 중)

## 🔧 개발 가이드

### 백엔드 (uv 사용)

```bash
cd backend

# 의존성 설치
uv sync

# 마이그레이션
uv run python manage.py migrate

# 관리자 계정 생성
uv run python manage.py createsuperuser

# 개발 서버 실행
uv run python manage.py runserver
```

### 프론트엔드

```bash
cd frontend/quasar-project

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev

# 빌드
npm run build
```

## 📝 환경 설정

### 백엔드 (.env)

```bash
cd backend
cp .env.example .env
# .env 파일 수정
```

### 프론트엔드

개발 환경: `.env.development` (기본 제공)
스테이징 환경: `.env.staging` (기본 제공)

## 🔒 보안

- 세션 기반 인증
- CSRF 토큰 보호
- 사용자별 데이터 격리
- CORS 설정

## 📚 API 문서

Swagger UI: http://localhost:8000/api/docs/
OpenAPI Schema: http://localhost:8000/api/schema/

## 🛠️ 유용한 명령어

### 백엔드

```bash
# Django 셸
uv run python manage.py shell

# 테스트
uv run python manage.py test

# 마이그레이션 파일 생성
uv run python manage.py makemigrations
```

### 프론트엔드

```bash
# 린트
npm run lint

# 타입 체크 (TypeScript 사용 시)
npm run type-check
```

## 📄 라이선스

MIT
