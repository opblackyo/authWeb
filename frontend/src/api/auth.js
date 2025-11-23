import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json'
  }
})

// 請求攔截器：添加 token
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 回應攔截器：處理錯誤
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.clearAuth()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authApi = {
  // 驗證碼 API
  getCaptcha: () => {
    return api.get('/api/captcha')
  },

  // 身份驗證 API
  login: (username, password, captchaAnswer, captchaToken) => {
    return api.post('/api/login', {
      username,
      password,
      captcha_answer: captchaAnswer,
      captcha_token: captchaToken
    })
  },

  register: (username, password, confirmPassword) => {
    return api.post('/api/register', {
      username,
      password,
      confirm_password: confirmPassword
    })
  },

  // 帳號管理 API
  getProfile: () => {
    return api.get('/api/profile')
  },

  changeUsername: (newUsername) => {
    return api.post('/api/user/username', {
      new_username: newUsername
    })
  },

  changePassword: (oldPassword, newPassword, confirmPassword) => {
    return api.post('/api/user/password', {
      old_password: oldPassword,
      new_password: newPassword,
      confirm_password: confirmPassword
    })
  },

  // OAuth 登入 API
  lineLoginInit: () => {
    return api.get('/api/login/line/init')
  },

  googleLoginInit: () => {
    return api.get('/api/login/google/init')
  },

  // OAuth 綁定 API
  lineLinkInit: () => {
    return api.get('/api/link/line/init')
  },

  googleLinkInit: () => {
    return api.get('/api/link/google/init')
  }
}
