import config from '../config'

// API 기본 클래스
class ApiService {
  constructor() {
    this.baseURL = config.api.baseURL
    this.timeout = config.api.timeout
  }

  // 기본 fetch 래퍼
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
      },
      ...options
    }

    if (config.app.debug) {
      console.log(`🌐 API Request: ${options.method || 'GET'} ${url}`)
    }

    try {
      const response = await fetch(url, defaultOptions)
      
      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`)
      }

      const data = await response.json()
      
      if (config.app.debug) {
        console.log(`✅ API Response:`, data)
      }
      
      return data
    } catch (error) {
      console.error(`❌ API Error:`, error)
      throw error
    }
  }

  // HTTP 메서드들
  get(endpoint) {
    return this.request(endpoint, { method: 'GET' })
  }

  post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT', 
      body: JSON.stringify(data)
    })
  }

  delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' })
  }
}

export default new ApiService()
