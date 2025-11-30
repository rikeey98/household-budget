# 🚀 운영 환경 배포 가이드

현재 로컬 개발 환경에서 실제 운영 환경으로 배포하는 방법을 설명합니다.

---

## 📋 목차

1. [현재 상태](#현재-상태)
2. [배포 옵션 비교](#배포-옵션-비교)
3. [옵션 1: Railway 배포 (추천)](#옵션-1-railway-배포-추천)
4. [옵션 2: Render 배포](#옵션-2-render-배포)
5. [옵션 3: DigitalOcean 서버 배포](#옵션-3-digitalocean-서버-배포)
6. [데이터 마이그레이션](#데이터-마이그레이션)
7. [보안 체크리스트](#보안-체크리스트)

---

## 현재 상태

### 개발 환경 (로컬)
```
- 데이터베이스: SQLite3 (db.sqlite3)
- 세션 저장: 데이터베이스
- 접속: localhost:8000만 가능
- 사용자 계정: 로컬 파일에 저장
```

### 운영 환경 (목표)
```
- 데이터베이스: PostgreSQL (별도 서버)
- 세션 저장: 데이터베이스/Redis
- 접속: 인터넷 어디서나 가능
- HTTPS 보안 연결
- 자동 백업
```

---

## 배포 옵션 비교

| 플랫폼 | 난이도 | 월 비용 | 무료 플랜 | 추천도 | 특징 |
|--------|--------|---------|-----------|--------|------|
| **Railway** | ⭐ 쉬움 | $5~ | ✅ $5 크레딧 | ⭐⭐⭐⭐⭐ | GitHub 연동, PostgreSQL 자동 |
| **Render** | ⭐ 쉬움 | $7~ | ✅ 제한적 | ⭐⭐⭐⭐ | 무료 PostgreSQL |
| **Heroku** | ⭐⭐ 보통 | $7~ | ❌ | ⭐⭐⭐ | 2022년부터 무료 플랜 종료 |
| **DigitalOcean** | ⭐⭐⭐ 어려움 | $6~ | ❌ | ⭐⭐⭐⭐ | 완전한 제어, 학습용 |
| **AWS/GCP** | ⭐⭐⭐⭐ 매우 어려움 | $10~ | ✅ 1년 | ⭐⭐⭐ | 엔터프라이즈급 |

---

## 옵션 1: Railway 배포 (추천)

### 장점
- ✅ **가장 간단한 배포 방법**
- ✅ GitHub 푸시만으로 자동 배포
- ✅ PostgreSQL 자동 설정
- ✅ 무료 $5 크레딧 제공 (월)
- ✅ HTTPS 자동 설정
- ✅ 도메인 자동 제공

### 단계별 가이드

#### 1. Railway 회원가입
```
https://railway.app/
→ Sign up with GitHub
```

#### 2. 새 프로젝트 생성
```
Dashboard → New Project
→ Deploy from GitHub repo
→ household-budget 선택
→ backend 폴더 선택
```

#### 3. PostgreSQL 추가
```
프로젝트에서 → New → Database → PostgreSQL
→ 자동으로 환경변수가 설정됨
```

#### 4. 환경변수 설정
```
Settings → Variables 메뉴에서 다음 추가:

SECRET_KEY=<Django secret key - 자동 생성>
DJANGO_SETTINGS_MODULE=household_budget.settings.prod
ALLOWED_HOSTS=.railway.app,.vercel.app
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
```

**SECRET_KEY 생성 방법:**
로컬에서 실행:
```bash
cd backend
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 5. 배포 완료!
```
GitHub에 푸시하면 자동으로 배포됨
→ Settings → Domains에서 URL 확인
→ https://household-budget-production.railway.app
```

#### 6. 관리자 계정 생성
```
Railway Console에서:
→ Settings → Deploy logs 확인
→ 배포 완료 후 아래 명령 실행

python manage.py shell -c "
from apps.accounts.models import User
User.objects.create_superuser('admin', 'admin@example.com', 'your-password')
"
```

---

## 옵션 2: Render 배포

### 단계별 가이드

#### 1. Render 회원가입
```
https://render.com/
→ Sign up with GitHub
```

#### 2. PostgreSQL 생성
```
Dashboard → New → PostgreSQL
→ Name: household-budget-db
→ Region: Singapore
→ Plan: Free
→ Create Database
```

#### 3. Web Service 생성
```
Dashboard → New → Web Service
→ Connect GitHub repo: household-budget
→ Root Directory: backend
→ Environment: Python 3
→ Build Command: uv sync
→ Start Command: uv run gunicorn household_budget.wsgi:application
```

#### 4. 환경변수 설정
```
Environment 탭에서:

SECRET_KEY=<생성한 키>
DJANGO_SETTINGS_MODULE=household_budget.settings.prod
ALLOWED_HOSTS=.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app

# PostgreSQL (자동 생성됨)
DATABASE_URL=<Render PostgreSQL URL>
```

#### 5. 배포 완료
```
→ https://household-budget.onrender.com
```

---

## 옵션 3: DigitalOcean 서버 배포

**권장 대상:** 서버 관리 경험이 있거나 학습하고 싶은 경우

### 1. Droplet 생성
```
- OS: Ubuntu 22.04 LTS
- Plan: Basic $6/월 (1GB RAM)
- Region: Singapore
- SSH Key 등록
```

### 2. 서버 접속 및 초기 설정
```bash
ssh root@your-server-ip

# 시스템 업데이트
apt update && apt upgrade -y

# 필수 패키지 설치
apt install -y python3.10 python3-pip postgresql postgresql-contrib nginx git

# uv 설치
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
```

### 3. PostgreSQL 설정
```bash
# PostgreSQL 시작
systemctl start postgresql
systemctl enable postgresql

# 데이터베이스 생성
sudo -u postgres psql << EOF
CREATE DATABASE household_budget;
CREATE USER budget_user WITH PASSWORD 'strong-password-here';
GRANT ALL PRIVILEGES ON DATABASE household_budget TO budget_user;
ALTER DATABASE household_budget OWNER TO budget_user;
\q
EOF
```

### 4. 프로젝트 배포
```bash
# 프로젝트 클론
cd /var/www
git clone https://github.com/your-username/household-budget.git
cd household-budget/backend

# 운영용 .env 생성
cat > .env << 'EOF'
SECRET_KEY=your-generated-secret-key
DJANGO_SETTINGS_MODULE=household_budget.settings.prod

POSTGRES_DB=household_budget
POSTGRES_USER=budget_user
POSTGRES_PASSWORD=strong-password-here
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
EOF

# 의존성 설치 및 마이그레이션
uv sync
uv run python manage.py migrate
uv run python manage.py collectstatic --noinput

# 관리자 계정 생성
uv run python manage.py shell -c "
from apps.accounts.models import User
User.objects.create_superuser('admin', 'admin@example.com', 'admin-password')
"
```

### 5. Gunicorn 설정
```bash
# Systemd 서비스 파일
cat > /etc/systemd/system/household-budget.service << EOF
[Unit]
Description=Household Budget Django
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/household-budget/backend
Environment="PATH=/var/www/household-budget/backend/.venv/bin"
ExecStart=/var/www/household-budget/backend/.venv/bin/gunicorn \\
    --workers 3 \\
    --bind unix:/var/www/household-budget/backend/gunicorn.sock \\
    household_budget.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# 서비스 시작
systemctl daemon-reload
systemctl start household-budget
systemctl enable household-budget
```

### 6. Nginx 설정
```bash
cat > /etc/nginx/sites-available/household-budget << 'EOF'
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location /static/ {
        alias /var/www/household-budget/backend/static/;
    }

    location /media/ {
        alias /var/www/household-budget/backend/media/;
    }

    location / {
        proxy_pass http://unix:/var/www/household-budget/backend/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

ln -s /etc/nginx/sites-available/household-budget /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### 7. SSL 인증서 (HTTPS)
```bash
# Certbot 설치
apt install -y certbot python3-certbot-nginx

# SSL 인증서 발급
certbot --nginx -d your-domain.com -d www.your-domain.com

# 자동 갱신
systemctl enable certbot.timer
```

---

## 데이터 마이그레이션

로컬 개발 데이터를 운영 환경으로 이전하는 방법:

### 방법 1: Django dumpdata/loaddata

```bash
# 로컬에서 데이터 내보내기
cd backend
uv run python manage.py dumpdata --natural-foreign --natural-primary \
  -e contenttypes -e auth.Permission \
  --indent 2 > data.json

# 운영 서버에서 데이터 가져오기
uv run python manage.py loaddata data.json
```

### 방법 2: PostgreSQL dump (운영 → 운영)

```bash
# 백업
pg_dump -U budget_user household_budget > backup.sql

# 복원
psql -U budget_user household_budget < backup.sql
```

---

## 보안 체크리스트

### ✅ 필수 보안 설정

- [ ] `DEBUG = False` 확인
- [ ] `SECRET_KEY` 환경변수로 관리
- [ ] `ALLOWED_HOSTS` 실제 도메인으로 제한
- [ ] `CORS_ALLOWED_ORIGINS` 프론트엔드 도메인만 허용
- [ ] HTTPS 적용 (SSL 인증서)
- [ ] PostgreSQL 강력한 비밀번호 사용
- [ ] 관리자 계정 강력한 비밀번호
- [ ] `.env` 파일 `.gitignore`에 포함
- [ ] 방화벽 설정 (필요한 포트만 열기)
- [ ] 정기 백업 설정

### 🔐 환경변수 체크

```bash
# 운영 환경에서 필수 환경변수
SECRET_KEY=<강력한 키>
DJANGO_SETTINGS_MODULE=household_budget.settings.prod
ALLOWED_HOSTS=your-domain.com
CORS_ALLOWED_ORIGINS=https://your-frontend.com

# PostgreSQL
POSTGRES_DB=household_budget
POSTGRES_USER=budget_user
POSTGRES_PASSWORD=<강력한 비밀번호>
POSTGRES_HOST=<DB 서버 주소>
POSTGRES_PORT=5432
```

---

## 프론트엔드 배포

### Vercel 배포 (추천)

```bash
# frontend/quasar-project 디렉토리에서
npm install -g vercel
vercel login
vercel

# 환경변수 설정
vercel env add VITE_API_URL
# → production으로 입력: https://your-backend.railway.app
```

### Netlify 배포

```bash
# frontend/quasar-project 디렉토리에서
npm run build

# dist/spa 폴더를 Netlify에 업로드
# 환경변수: VITE_API_URL=https://your-backend.railway.app
```

---

## 모니터링 및 유지보수

### 로그 확인

**Railway/Render:**
```
Dashboard → Logs 탭에서 실시간 확인
```

**DigitalOcean:**
```bash
# Django 로그
journalctl -u household-budget -f

# Nginx 로그
tail -f /var/log/nginx/error.log
```

### 정기 백업

**자동 백업 스크립트 (DigitalOcean):**
```bash
cat > /root/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U budget_user household_budget > /backups/db_$DATE.sql
find /backups -name "db_*.sql" -mtime +7 -delete
EOF

chmod +x /root/backup.sh

# 매일 새벽 2시 백업
echo "0 2 * * * /root/backup.sh" | crontab -
```

---

## 문제 해결

### 1. "DisallowedHost" 에러
```
→ ALLOWED_HOSTS에 도메인 추가
ALLOWED_HOSTS=your-domain.com,.railway.app
```

### 2. CORS 에러
```
→ CORS_ALLOWED_ORIGINS 확인
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

### 3. 정적 파일 404
```bash
# collectstatic 다시 실행
uv run python manage.py collectstatic --noinput
```

### 4. 데이터베이스 연결 실패
```
→ PostgreSQL 환경변수 확인
→ 네트워크/방화벽 확인
```

---

## 참고 자료

- [Django 배포 체크리스트](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Railway 문서](https://docs.railway.app/)
- [Render 문서](https://render.com/docs)
- [DigitalOcean 튜토리얼](https://www.digitalocean.com/community/tutorials)
- [Gunicorn 문서](https://docs.gunicorn.org/)

---

## 추천 배포 플랜

### 초보자
1. **Railway** - 가장 쉽고 빠름
2. GitHub 연동으로 자동 배포
3. $5/월 크레딧 활용

### 학습 목적
1. **DigitalOcean** - 서버 관리 학습
2. 완전한 제어권
3. Linux/Nginx/PostgreSQL 경험

### 프로덕션
1. **AWS/GCP** - 확장성 필요 시
2. **DigitalOcean** - 중소규모
3. 모니터링 및 백업 필수
