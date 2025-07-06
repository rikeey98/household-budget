// 환경별 설정 관리
export const config = {
  // API 설정
  api: {
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    timeout: 10000,
    endpoints: {
      auth: '/api/auth',
      transactions: '/api/transactions',
      categories: '/api/categories',
      statistics: '/api/statistics',
      test: '/api/test'
    }
  },
  
  // 앱 설정
  app: {
    title: import.meta.env.VITE_APP_TITLE || '가계부',
    version: '1.0.0',
    debug: import.meta.env.VITE_DEBUG === 'true',
    logLevel: import.meta.env.VITE_LOG_LEVEL || 'info'
  },
  
  // UI 설정
  ui: {
    pageSize: 20,
    dateFormat: 'YYYY-MM-DD',
    currency: 'KRW',
    theme: {
      primary: '#1976d2',
      secondary: '#26a69a',
      accent: '#9c27b0',
      dark: '#1d1d1d',
      positive: '#21ba45',
      negative: '#c10015',
      info: '#31ccec',
      warning: '#f2c037'
    }
  },
  
  // 개발 환경 확인
  isDevelopment: import.meta.env.DEV,
  isProduction: import.meta.env.PROD,
  
  // 환경 정보
  getEnvironment() {
    if (import.meta.env.MODE === 'production') return 'production'
    if (import.meta.env.MODE === 'staging') return 'staging'
    if (import.meta.env.MODE === 'development') return 'development'
    return 'local'
  }
}

// 개발 환경에서만 설정 정보 출력
if (config.app.debug) {
  console.log('🔧 App Configuration:', config)
  console.log('🌍 Environment:', config.getEnvironment())
  console.log('🔗 API Base URL:', config.api.baseURL)
}

export default config
