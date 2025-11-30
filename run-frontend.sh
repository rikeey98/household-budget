#!/bin/bash
# 프론트엔드 개발 서버 실행 스크립트

cd frontend/quasar-project

# node_modules가 없으면 설치
if [ ! -d "node_modules" ]; then
    echo "📦 패키지를 설치합니다..."
    npm install
fi

echo "🚀 Quasar 개발 서버를 시작합니다..."
npm run dev
