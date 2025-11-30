#!/bin/bash
# Django 개발 서버 실행 스크립트 (uv 버전)

export PATH="$HOME/.local/bin:$PATH"

echo "🚀 Django 개발 서버를 시작합니다..."

# 마이그레이션 확인
if [ ! -f "db.sqlite3" ]; then
    echo "📦 데이터베이스 마이그레이션을 실행합니다..."
    uv run python manage.py migrate
fi

# 개발 서버 실행
uv run python manage.py runserver
