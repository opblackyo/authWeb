<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="title">登入</h1>
      <form @submit.prevent="handleLogin" class="form">
        <div class="form-group">
          <label for="username">使用者名稱</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            placeholder="請輸入使用者名稱"
            class="input"
          />
        </div>
        <div class="form-group">
          <label for="password">密碼</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            placeholder="請輸入密碼"
            class="input"
          />
        </div>
        <div class="form-group">
          <label for="captcha">驗證碼</label>
          <input
            id="captcha"
            v-model="form.captchaAnswer"
            type="text"
            required
            placeholder="請輸入驗證碼"
            class="input captcha-input"
            maxlength="6"
          />
          <div class="captcha-image-container">
            <img
              v-if="captchaImage"
              :src="captchaImage"
              alt="驗證碼"
              class="captcha-image"
              @click="refreshCaptcha"
            />
            <button
              v-else
              type="button"
              @click="loadCaptcha"
              class="captcha-load-button"
            >
              載入驗證碼
            </button>
          </div>
          <button
            type="button"
            @click="refreshCaptcha"
            class="refresh-captcha-button"
          >
            重新載入驗證碼
          </button>
        </div>
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        <button type="submit" :disabled="loading || !captchaToken" class="submit-button">
          {{ loading ? '登入中...' : '登入' }}
        </button>
        <div class="oauth-buttons">
          <button
            type="button"
            @click="handleLineLogin"
            class="oauth-button line-button"
          >
            LINE 登入
          </button>
          <button
            type="button"
            @click="handleGoogleLogin"
            class="oauth-button google-button"
          >
            Google 登入
          </button>
        </div>
        <div class="link-container">
          <span>還沒有帳號？</span>
          <router-link to="/register" class="link">立即註冊</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { authApi } from '@/api/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  password: '',
  captchaAnswer: ''
})

const loading = ref(false)
const error = ref('')
const captchaImage = ref('')
const captchaToken = ref('')

const loadCaptcha = async () => {
  try {
    const response = await authApi.getCaptcha()
    captchaImage.value = response.data.image
    captchaToken.value = response.data.captcha_token
  } catch (err) {
    error.value = '載入驗證碼失敗，請重新整理頁面'
  }
}

const refreshCaptcha = () => {
  form.value.captchaAnswer = ''
  loadCaptcha()
}

const handleLogin = async () => {
  error.value = ''
  
  if (!form.value.captchaAnswer || !captchaToken.value) {
    error.value = '請先載入並輸入驗證碼'
    return
  }
  
  loading.value = true

  const result = await authStore.login(
    form.value.username,
    form.value.password,
    form.value.captchaAnswer,
    captchaToken.value
  )

  if (result.success) {
    router.push('/')
  } else {
    error.value = result.error
    // 登入失敗後重新載入驗證碼
    refreshCaptcha()
  }

  loading.value = false
}

const handleLineLogin = async () => {
  try {
    const response = await authApi.lineLoginInit()
    window.location.href = response.data.auth_url
  } catch (err) {
    error.value = 'LINE 登入初始化失敗'
  }
}

const handleGoogleLogin = async () => {
  try {
    const response = await authApi.googleLoginInit()
    window.location.href = response.data.auth_url
  } catch (err) {
    error.value = 'Google 登入初始化失敗'
  }
}

onMounted(() => {
  loadCaptcha()
})
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 12px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin-bottom: 30px;
  text-align: center;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: #555;
}

.input {
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.input:focus {
  outline: none;
  border-color: #667eea;
}

.captcha-input {
  margin-bottom: 10px;
}

.captcha-image-container {
  margin-bottom: 10px;
}

.captcha-image {
  width: 120px;
  height: 50px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: border-color 0.3s;
}

.captcha-image:hover {
  border-color: #667eea;
}

.captcha-load-button {
  width: 120px;
  height: 50px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: #f5f5f5;
  cursor: pointer;
  font-size: 12px;
}

.refresh-captcha-button {
  padding: 6px 12px;
  background: #f5f5f5;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  align-self: flex-start;
  transition: background 0.3s;
}

.refresh-captcha-button:hover {
  background: #e0e0e0;
}

.error-message {
  color: #e74c3c;
  font-size: 14px;
  padding: 10px;
  background: #fee;
  border-radius: 6px;
  border: 1px solid #fcc;
}

.submit-button {
  padding: 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.3s;
}

.submit-button:hover:not(:disabled) {
  opacity: 0.9;
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.oauth-buttons {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.oauth-button {
  flex: 1;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.line-button {
  background: #06C755;
  color: white;
  border-color: #06C755;
}

.line-button:hover {
  background: #05b04a;
  border-color: #05b04a;
}

.google-button {
  background: white;
  color: #4285F4;
  border-color: #4285F4;
}

.google-button:hover {
  background: #f0f7ff;
}

.link-container {
  text-align: center;
  margin-top: 20px;
  color: #666;
  font-size: 14px;
}

.link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  margin-left: 5px;
}

.link:hover {
  text-decoration: underline;
}
</style>
