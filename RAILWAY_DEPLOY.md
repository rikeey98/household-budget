# 🚂 Railway 백엔드 배포 가이드 (2024 최신)

Railway 최신 UI 기준으로 작성된 상세 배포 가이드입니다.

---

## 📋 사전 준비

### 1. GitHub 저장소에 코드 푸시
```bash
git add .
git commit -m "feat: 배포 준비"
git push origin main
```

### 2. SECRET_KEY 생성 (로컬에서 실행)
```bash
cd backend
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**생성된 키를 복사해두세요!**
예시: `kn3mhv&r)uf3+mhi!*dqf#zx3_4a(b!ai#ho*qq056(4^^50l&`

---

## 🚀 Step 1: Railway 프로젝트 생성

### 1.1 회원가입
```
1. https://railway.app/ 접속
2. "Start a New Project" 버튼 클릭
3. "Login with GitHub" 선택
4. GitHub 계정 인증 완료
```

### 1.2 새 프로젝트 생성
```
1. Dashboard 화면에서 "+ New Project" 클릭
2. "Deploy from GitHub repo" 선택
3. "Configure GitHub App" → 저장소 접근 권한 부여
4. "household-budget" 저장소 선택
5. 자동으로 배포 시작됨 (잠시 대기)
```

---

## 🗄️ Step 2: PostgreSQL 데이터베이스 추가

### 2.1 데이터베이스 생성
```
1. 프로젝트 화면 (캔버스 뷰)에서
2. 우측 상단 "+ New" 버튼 클릭
3. "Database" 선택
4. "Add PostgreSQL" 클릭
5. PostgreSQL 서비스가 자동 생성됨
```

### 2.2 데이터베이스 환경변수 확인
```
1. PostgreSQL 서비스 클릭
2. "Variables" 탭 클릭
3. 다음 변수들이 자동 생성되어 있는지 확인:
   - DATABASE_URL
   - PGHOST
   - PGPORT
   - PGUSER
   - PGPASSWORD
   - PGDATABASE
```

---

## ⚙️ Step 3: 백엔드 서비스 설정

### 3.1 서비스 선택
프로젝트에 2개의 서비스가 있습니다:
- **household-budget** ← 이것을 클릭!
- postgres

### 3.2 Root Directory 설정

**중요! 백엔드 폴더만 배포하도록 설정**

```
1. household-budget 서비스 클릭
2. "Settings" 탭 클릭
3. "General" 섹션에서 스크롤
4. "Root Directory" 찾기
5. 값 입력: backend
6. 자동 저장됨
```

### 3.3 환경변수 설정

**Variables 탭 위치 (최신 UI):**

```
옵션 1: household-budget 서비스 클릭 → Variables 탭 (상단)
옵션 2: household-budget 서비스 클릭 → Settings → Variables (사이드바)
```

**UI가 보이지 않는 경우:**
- 서비스 이름(household-budget) 클릭 확인
- 상단 탭 메뉴에서 "Variables" 찾기
- 또는 "Settings" → 왼쪽 "Variables" 메뉴

**추가할 환경변수 (Raw Editor 사용 추천):**

Variables 탭에서 "Raw Editor" 버튼 클릭 후 다음 내용 붙여넣기:

```bash
# Django 설정
SECRET_KEY=<위에서 생성한 SECRET_KEY 붙여넣기>
DJANGO_SETTINGS_MODULE=household_budget.settings.prod

# 허용 호스트 (Railway 자동 도메인)
ALLOWED_HOSTS=.railway.app

# PostgreSQL 연결 (Railway가 자동으로 주입)
POSTGRES_DB=${PGDATABASE}
POSTGRES_USER=${PGUSER}
POSTGRES_PASSWORD=${PGPASSWORD}
POSTGRES_HOST=${PGHOST}
POSTGRES_PORT=${PGPORT}

# CORS 설정 (나중에 프론트엔드 배포 후 수정)
CORS_ALLOWED_ORIGINS=http://localhost:9000
```

**변수 하나씩 추가하는 경우:**

```
1. Variables 탭에서
2. "New Variable" 버튼 클릭
3. Variable name: SECRET_KEY
4. Value: <생성한 SECRET_KEY>
5. "Add" 버튼 클릭
6. 나머지 변수들도 같은 방식으로 추가
```

---

## 🔨 Step 4: 빌드 설정

### 4.1 Build Command 설정

```
1. Settings 탭 클릭
2. "Deploy" 섹션 찾기
3. "Custom Build Command" 입력:
   uv sync && uv run python manage.py collectstatic --noinput
4. 저장됨
```

### 4.2 Start Command 설정

```
1. 같은 "Deploy" 섹션에서
2. "Custom Start Command" 입력:
   uv run python manage.py migrate && uv run gunicorn household_budget.wsgi:application --bind 0.0.0.0:$PORT
3. 저장됨
```

---

## 📝 Step 5: railway.toml 파일 생성 (추천)

**또는** 위 설정을 파일로 관리하려면:

backend/railway.toml 파일이 이미 존재합니다. 내용 확인:

```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uv run python manage.py migrate && uv run python manage.py collectstatic --noinput && uv run gunicorn household_budget.wsgi:application --bind 0.0.0.0:$PORT"
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 10
```

이 파일이 있으면 Railway가 자동으로 읽습니다.

---

## 🚀 Step 6: 배포 실행

### 6.1 재배포 트리거

```
1. household-budget 서비스에서
2. "Deployments" 탭 클릭
3. 최신 배포 확인
4. 또는 우측 상단 "Deploy" 버튼 클릭
```

### 6.2 배포 로그 확인

```
1. "Deployments" 탭에서
2. 최신 배포 클릭
3. "View Logs" 또는 "Build Logs" 확인
4. 에러 메시지 확인
```

**성공 시 로그 예시:**
```
✓ Building
✓ Deploying
✓ Success
```

---

## 🌐 Step 7: 도메인 확인

### 7.1 Public URL 확인

```
1. household-budget 서비스에서
2. "Settings" 탭 클릭
3. "Networking" 섹션 찾기
4. "Public Networking" 활성화
5. "Generate Domain" 클릭
```

**생성된 도메인 예시:**
```
https://household-budget-production.up.railway.app
```

### 7.2 API 테스트

브라우저에서 다음 URL 접속:
```
https://your-app.railway.app/api/docs/
```

Swagger UI가 표시되면 성공!

---

## 👤 Step 8: 관리자 계정 생성

### Railway Console 사용

```
1. household-budget 서비스에서
2. "Settings" 탭 클릭
3. "Service" 섹션에서 "Open Service Shell" 또는 Console 찾기
4. 또는 Railway CLI 사용 (아래 참조)
```

**Railway CLI 설치 (권장):**

```bash
# macOS
brew install railway

# npm
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 연결
railway link

# Shell 접속
railway run bash

# 관리자 계정 생성
uv run python manage.py shell -c "
from apps.accounts.models import User
User.objects.create_superuser('admin', 'admin@example.com', 'your-admin-password')
print('관리자 계정 생성 완료!')
"
```

**또는 Django Admin에서 생성:**

1. https://your-app.railway.app/admin/ 접속
2. "회원가입" 기능 사용 (프론트엔드)
3. Railway Console에서 superuser로 승격:
```python
railway run uv run python manage.py shell -c "
from apps.accounts.models import User
user = User.objects.get(username='your-username')
user.is_staff = True
user.is_superuser = True
user.save()
"
```

---

## ✅ Step 9: 배포 확인 체크리스트

### 환경변수 확인
- [ ] SECRET_KEY 설정됨
- [ ] DJANGO_SETTINGS_MODULE=household_budget.settings.prod
- [ ] ALLOWED_HOSTS=.railway.app
- [ ] PostgreSQL 환경변수 자동 설정됨

### 서비스 설정 확인
- [ ] Root Directory = backend
- [ ] Build Command 설정
- [ ] Start Command 설정
- [ ] Public Networking 활성화

### 기능 확인
- [ ] https://your-app.railway.app/api/docs/ 접속 가능
- [ ] PostgreSQL 연결 성공
- [ ] 관리자 계정 생성 완료
- [ ] API 엔드포인트 정상 작동

---

## 🔧 문제 해결

### 1. "Variables" 탭이 보이지 않아요

**해결 방법:**
```
1. 서비스(household-budget)를 정확히 클릭했는지 확인
2. 상단 탭 메뉴 확인: Overview, Deployments, Metrics, Variables, Settings
3. Settings → 왼쪽 사이드바 "Variables" 메뉴 확인
4. 브라우저 새로고침 (Cmd/Ctrl + R)
5. 다른 브라우저로 시도
```

### 2. "Application failed to respond" 에러

**원인:**
- PORT 환경변수를 사용하지 않음
- Gunicorn이 잘못된 포트로 바인딩

**해결:**
```bash
# Start Command 확인
uv run gunicorn household_budget.wsgi:application --bind 0.0.0.0:$PORT

# $PORT 변수가 포함되어 있어야 함!
```

### 3. "DisallowedHost" 에러

**원인:**
- ALLOWED_HOSTS 미설정

**해결:**
```bash
# Variables에 추가
ALLOWED_HOSTS=.railway.app,.up.railway.app

# 또는
ALLOWED_HOSTS=*  # 임시로 테스트 (운영에는 비추천)
```

### 4. "relation does not exist" 에러

**원인:**
- 마이그레이션 미실행

**해결:**
```bash
# Railway Shell에서
railway run uv run python manage.py migrate

# 또는 Start Command에 포함 (이미 설정됨)
uv run python manage.py migrate && uv run gunicorn ...
```

### 5. PostgreSQL 연결 실패

**확인 사항:**
```
1. PostgreSQL 서비스가 생성되어 있는지
2. Variables에서 PGHOST, PGDATABASE 등 자동 생성 확인
3. prod.py에서 DATABASES 설정 확인
```

**prod.py 확인:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),      # ${PGDATABASE}
        'USER': os.getenv('POSTGRES_USER'),    # ${PGUSER}
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),  # ${PGPASSWORD}
        'HOST': os.getenv('POSTGRES_HOST'),    # ${PGHOST}
        'PORT': os.getenv('POSTGRES_PORT', '5432'),  # ${PGPORT}
    }
}
```

### 6. 정적 파일 404 에러

**해결:**
```bash
# Build Command에 collectstatic 포함 확인
uv sync && uv run python manage.py collectstatic --noinput

# 또는 수동 실행
railway run uv run python manage.py collectstatic --noinput
```

---

## 📊 배포 후 모니터링

### Metrics 확인
```
1. household-budget 서비스
2. "Metrics" 탭 클릭
3. CPU, Memory, Network 사용량 확인
```

### Logs 실시간 확인
```
1. "Deployments" 탭
2. 최신 배포 클릭
3. "View Logs" 클릭
4. 실시간 로그 스트림 확인
```

### Railway CLI로 로그 확인
```bash
railway logs
```

---

## 🔄 업데이트 배포

### 자동 배포 (GitHub 연동)
```bash
# 로컬에서 수정
git add .
git commit -m "feat: 새 기능 추가"
git push origin main

# Railway가 자동으로 감지하고 재배포함!
```

### 수동 배포
```
1. Railway Dashboard
2. household-budget 서비스
3. Deployments 탭
4. "Deploy" 버튼 클릭
```

---

## 💰 비용 관리

### Free Trial
- 첫 사용자: $5 크레딧 제공
- 시간당 약 $0.000463 (Hobby Plan)
- 무료 크레딧으로 약 10,000시간 사용 가능

### Hobby Plan ($5/월)
- 소규모 프로젝트에 충분
- PostgreSQL 포함
- 무제한 프로젝트

### 사용량 확인
```
1. Dashboard 우측 상단
2. 사용자 아이콘 클릭
3. "Usage" 확인
```

---

## 🎯 다음 단계

1. ✅ 백엔드 배포 완료
2. ⬜ 프론트엔드 Vercel 배포
3. ⬜ CORS 설정 업데이트
4. ⬜ 커스텀 도메인 연결 (선택)
5. ⬜ 백업 설정

---

## 📚 참고 링크

- [Railway 공식 문서](https://docs.railway.app/)
- [Railway CLI](https://docs.railway.app/develop/cli)
- [Django 배포 체크리스트](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Gunicorn 문서](https://docs.gunicorn.org/)

---

## 🆘 추가 도움말

문제가 해결되지 않으면:
1. Railway Discord: https://discord.gg/railway
2. GitHub Issues: 프로젝트 저장소
3. 배포 로그 확인 및 에러 메시지 복사

배포 성공을 기원합니다! 🚀
