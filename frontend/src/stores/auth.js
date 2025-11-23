import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)
  const userRole = computed(() => user.value?.role || 'customer')
  const isCustomer = computed(() => userRole.value === 'customer')
  const isMerchant = computed(() => userRole.value === 'merchant')

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

  const login = async (username, password, captchaAnswer, captchaToken) => {
    try {
      const response = await authApi.login(username, password, captchaAnswer, captchaToken)
      // API 返回格式: { message, token, user, role, display_name, email, phone, merchant?, expires_in }
      const userData = {
        username: response.data.user,
        role: response.data.role || 'customer',
        display_name: response.data.display_name,
        email: response.data.email,
        phone: response.data.phone,
        merchant: response.data.merchant
      }
      setAuth(response.data.token, userData)
      return { success: true, role: userData.role }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.message || '登入失敗'
      }
    }
  }

  const register = async (username, password, confirmPassword, role = 'customer', additionalData = {}) => {
    try {
      await authApi.register(username, password, confirmPassword, role, additionalData)
      return { success: true }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.message || '註冊失敗'
      }
    }
  }

  const logout = () => {
    clearAuth()
  }

  const fetchProfile = async () => {
    try {
      const response = await authApi.getProfile()
      // API 返回格式: { message, user_id, username, email, display_name, is_line_linked, is_google_linked }
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
      return { success: true, data: response.data }
    } catch (error) {
      if (error.response?.status === 401) {
        clearAuth()
      }
      return {
        success: false,
        error: error.response?.data?.message || '取得個人資料失敗'
      }
    }
  }

  const updateUsername = async (newUsername) => {
    try {
      const response = await authApi.changeUsername(newUsername)
      // API 返回新的 token，需要更新
      if (response.data.token) {
        setAuth(response.data.token, user.value)
      }
      return { success: true, data: response.data }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.message || '變更使用者名稱失敗'
      }
    }
  }

  const updatePassword = async (oldPassword, newPassword, confirmPassword) => {
    try {
      await authApi.changePassword(oldPassword, newPassword, confirmPassword)
      return { success: true }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.message || '變更密碼失敗'
      }
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    userRole,
    isCustomer,
    isMerchant,
    setAuth,
    clearAuth,
    login,
    register,
    logout,
    fetchProfile,
    updateUsername,
    updatePassword
  }
})
