import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/', // Django API 주소
  withCredentials: true, // ★ 세션 쿠키 자동 포함
});

export default api;
export { api };

// CSRF 토큰 받아오는 함수
export async function fetchCSRFToken() {
  const res = await api.get('accounts/auth/csrf/');
  // Django는 보통 { csrfToken: "..." } 형태로 응답
  return res.data.csrfToken;
}

// 로그인 함수
export async function login(username, password) {
  const csrfToken = await fetchCSRFToken();
  return api.post(
    'accounts/auth/login/',
    { username, password },
    {
      headers: {
        'X-CSRFToken': csrfToken,
      },
    }
  );
}

export async function getCurrentUser() {
  return api.get('accounts/auth/user/');
}

// 로그아웃 함수
export async function logout() {
  const csrfToken = await fetchCSRFToken();
  return api.post(
    'accounts/auth/logout/',
    {},
    {
      headers: {
        'X-CSRFToken': csrfToken,
      },
    }
  );
}

// 회원가입 함수
export async function register(data) {
  const csrfToken = await fetchCSRFToken();
  return api.post(
    'accounts/auth/register/',
    data,
    {
      headers: {
        'X-CSRFToken': csrfToken,
      },
    }
  );
}

// CSRF 토큰을 포함한 DELETE 요청 헬퍼
export async function deleteWithCSRF(url, config = {}) {
  const csrfToken = await fetchCSRFToken();
  return api.delete(url, {
    ...config,
    headers: {
      ...(config.headers || {}),
      'X-CSRFToken': csrfToken,
    },
  });
}
// api.delete 대신 deleteWithCSRF(url) 사용 권장

export async function postWithCSRF(url, data, config = {}) {
  const csrfToken = await fetchCSRFToken();
  return api.post(url, data, {
    ...config,
    headers: {
      ...(config.headers || {}),
      'X-CSRFToken': csrfToken,
    },
  });
}
