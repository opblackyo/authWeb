import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)

  const setAuth = (newToken, userData) => {
    token.value = newToken
    user.value = userData
    localStorage.setItem('token', newToken)
    localStorage.setItem('user', JSON.stringify(userData))
  }

  const clearAuth = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  const login = async (username, password) => {
    try {
      const response = await authApi.login(username, password)
      setAuth(response.data.access_token, response.data.user)
      return { success: true }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || '登入失敗'
      }
    }
  }

  const register = async (username, email, password) => {
    try {
      await authApi.register(username, email, password)
      return { success: true }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || '註冊失敗'
      }
    }
  }

  const logout = () => {
    clearAuth()
  }

  const fetchProfile = async () => {
    try {
      const response = await authApi.getProfile()
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
      return { success: true }
    } catch (error) {
      if (error.response?.status === 401) {
        clearAuth()
      }
      return {
        success: false,
        error: error.response?.data?.error || '取得個人資料失敗'
      }
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    fetchProfile
  }
})

