<template>
  <div class="login-container">
    <div class="login-card">
      <div class="header">
        <h1 class="title">歡迎回來</h1>
        <p class="subtitle">登入您的帳號繼續使用</p>
      </div>

      <form @submit.prevent="handleLogin" class="form">
        <!-- 使用者名稱 -->
        <BaseInput
          v-model="form.username"
          label="使用者名稱"
          placeholder="請輸入使用者名稱"
          icon="👤"
          required
        />

        <!-- 密碼 -->
        <BaseInput
          v-model="form.password"
          type="password"
          label="密碼"
          placeholder="請輸入密碼"
          icon="🔒"
          required
        />

        <!-- 驗證碼 -->
        <div class="captcha-group">
          <BaseInput
            v-model="form.captchaAnswer"
            label="驗證碼"
            placeholder="請輸入驗證碼"
            icon="🔐"
            maxlength="6"
            required
          />

          <div class="captcha-container">
            <div class="captcha-image-wrapper">
              <img
                v-if="captchaImage"
                :src="captchaImage"
                alt="驗證碼"
                class="captcha-image"
                @click="refreshCaptcha"
                title="點擊重新載入"
              />
              <BaseButton
                v-else
                type="button"
                variant="outline"
                size="small"
                @click="loadCaptcha"
              >
                載入驗證碼
              </BaseButton>
            </div>

            <BaseButton
              type="button"
              variant="ghost"
              size="small"
              icon="🔄"
              @click="refreshCaptcha"
            >
              重新載入
            </BaseButton>
          </div>
        </div>

        <!-- 錯誤訊息 -->
        <div v-if="error" class="error-message">
          <span class="error-icon">⚠️</span>
          {{ error }}
        </div>

        <!-- 登入按鈕 -->
        <BaseButton
          type="submit"
          variant="primary"
          size="large"
          :loading="loading"
          :disabled="!captchaToken"
        >
          {{ loading ? '登入中...' : '立即登入' }}
        </BaseButton>

        <!-- OAuth 登入 -->
        <div class="divider">
          <span>或使用以下方式登入</span>
        </div>

        <div class="oauth-buttons">
          <BaseButton
            type="button"
            variant="outline"
            size="medium"
            @click="handleLineLogin"
            class="oauth-button line-button"
          >
            <span class="oauth-icon">💬</span>
            LINE 登入
          </BaseButton>

          <BaseButton
            type="button"
            variant="outline"
            size="medium"
            @click="handleGoogleLogin"
            class="oauth-button google-button"
          >
            <span class="oauth-icon">🔍</span>
            Google 登入
          </BaseButton>
        </div>

        <!-- 註冊連結 -->
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
import BaseInput from '@/components/common/BaseInput.vue'
import BaseButton from '@/components/common/BaseButton.vue'

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
    // 根據角色導向不同頁面
    if (result.role === 'merchant') {
      router.push('/dashboard')  // 商家導向 Dashboard
    } else {
      router.push('/')  // 顧客導向首頁（未來改為餐廳首頁）
    }
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  background: white;
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.title {
  font-size: 32px;
  font-weight: 700;
  color: #333;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 16px;
  color: #666;
  margin: 0;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 驗證碼組 */
.captcha-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.captcha-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.captcha-image-wrapper {
  flex-shrink: 0;
}

.captcha-image {
  width: 140px;
  height: 50px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  display: block;
}

.captcha-image:hover {
  border-color: #667eea;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
}

/* 錯誤訊息 */
.error-message {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #e74c3c;
  font-size: 14px;
  padding: 12px 16px;
  background: #fee;
  border-radius: 8px;
  border: 1px solid #fcc;
}

.error-icon {
  font-size: 18px;
}

/* 分隔線 */
.divider {
  position: relative;
  text-align: center;
  margin: 10px 0;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #e0e0e0;
}

.divider span {
  position: relative;
  display: inline-block;
  padding: 0 15px;
  background: white;
  color: #999;
  font-size: 13px;
}

/* OAuth 按鈕 */
.oauth-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.oauth-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.oauth-icon {
  font-size: 18px;
}

.line-button {
  border-color: #06C755 !important;
  color: #06C755 !important;
}

.line-button:hover {
  background: #06C755 !important;
  color: white !important;
}

.google-button {
  border-color: #4285F4 !important;
  color: #4285F4 !important;
}

.google-button:hover {
  background: #4285F4 !important;
  color: white !important;
}

/* 連結容器 */
.link-container {
  text-align: center;
  margin-top: 10px;
  color: #666;
  font-size: 14px;
}

.link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  margin-left: 5px;
  transition: color 0.3s;
}

.link:hover {
  color: #764ba2;
  text-decoration: underline;
}

/* 響應式設計 */
@media (max-width: 640px) {
  .login-card {
    padding: 30px 20px;
  }

  .title {
    font-size: 26px;
  }

  .oauth-buttons {
    grid-template-columns: 1fr;
  }

  .captcha-container {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
