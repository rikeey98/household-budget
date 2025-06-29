// 환경 설정 작동 원리 데모
console.log('=== 환경 설정 작동 원리 ===')

// 1. Vite는 다음 순서로 .env 파일을 로드합니다:
console.log('📁 Vite .env 파일 로드 순서:')
console.log('1. .env.[mode].local (우선순위 높음, git 무시)')
console.log('2. .env.[mode] (환경별: development, staging, production)')
console.log('3. .env.local (git 무시)')
console.log('4. .env (기본값, 우선순위 낮음)')

// 2. 현재 로드된 환경 변수들
console.log('\n🔧 현재 로드된 환경 변수:')
const env = import.meta.env
Object.keys(env).forEach(key => {
  if (key.startsWith('VITE_')) {
    console.log(`${key}: ${env[key]}`)
  }
})

// 3. 환경 감지
console.log('\n🌍 환경 감지:')
console.log(`MODE: ${import.meta.env.MODE}`)
console.log(`DEV: ${import.meta.env.DEV}`)
console.log(`PROD: ${import.meta.env.PROD}`)

// 4. 환경에 따른 다른 동작 예시
if (import.meta.env.VITE_DEBUG === 'true') {
  console.log('🐛 디버그 모드가 활성화되었습니다!')
  console.log('상세한 로그를 출력합니다.')
} else {
  console.log('🔒 운영 모드 - 디버그 로그가 비활성화되었습니다.')
}

export default {
  message: '환경 설정 데모 완료'
}
