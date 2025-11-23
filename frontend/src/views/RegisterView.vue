<template>
  <div class="register-container">
    <div class="register-card">
      <div class="header">
        <h1 class="title">註冊帳號</h1>
        <p class="subtitle">選擇您的身分開始使用</p>
      </div>

      <form @submit.prevent="handleRegister" class="form">
        <!-- 角色選擇 -->
        <div class="role-selector">
          <div
            class="role-card"
            :class="{ active: form.role === 'customer' }"
            @click="selectRole('customer')"
          >
            <div class="role-icon">👥</div>
            <div class="role-name">顧客</div>
            <div class="role-desc">瀏覽餐廳、下訂單</div>
          </div>
          <div
            class="role-card"
            :class="{ active: form.role === 'merchant' }"
            @click="selectRole('merchant')"
          >
            <div class="role-icon">🏪</div>
            <div class="role-name">商家</div>
            <div class="role-desc">管理餐廳、接訂單</div>
          </div>
        </div>

        <!-- 基本資訊 -->
        <BaseInput
          v-model="form.username"
          label="使用者名稱"
          placeholder="請輸入使用者名稱（至少 4 個字元）"
          icon="👤"
          :error="errors.username"
          required
        />

        <BaseInput
          v-model="form.password"
          type="password"
          label="密碼"
          placeholder="請輸入密碼（至少 6 個字元）"
          icon="🔒"
          :error="errors.password"
          hint="密碼至少需要 6 個字元"
          required
        />

        <BaseInput
          v-model="form.confirmPassword"
          type="password"
          label="確認密碼"
          placeholder="請再次輸入密碼"
          icon="🔒"
          :error="errors.confirmPassword"
          required
        />

        <!-- 額外資訊 -->
        <BaseInput
          v-model="form.displayName"
          label="顯示名稱"
          placeholder="請輸入顯示名稱（選填）"
          icon="✨"
        />

        <BaseInput
          v-model="form.email"
          type="email"
          label="電子郵件"
          placeholder="請輸入電子郵件（選填）"
          icon="📧"
        />

        <BaseInput
          v-model="form.phone"
          type="tel"
          label="電話號碼"
          placeholder="請輸入電話號碼（選填）"
          icon="📱"
        />

        <!-- 商家專用欄位 -->
        <div v-if="form.role === 'merchant'" class="merchant-fields">
          <div class="section-title">
            <span class="icon">🏪</span>
            <span>商家資訊</span>
          </div>

          <BaseInput
            v-model="form.businessName"
            label="商家名稱"
            placeholder="請輸入商家名稱"
            icon="🏷️"
            :error="errors.businessName"
            required
          />

          <BaseInput
            v-model="form.businessType"
            label="商家類型"
            placeholder="例如：中式料理、日式料理、咖啡廳"
            icon="🍽️"
          />

          <BaseInput
            v-model="form.address"
            label="商家地址"
            placeholder="請輸入商家地址（選填）"
            icon="📍"
          />
        </div>

        <!-- 錯誤訊息 -->
        <div v-if="error" class="error-message">
          <span class="error-icon">⚠️</span>
          {{ error }}
        </div>

        <!-- 成功訊息 -->
        <div v-if="success" class="success-message">
          <span class="success-icon">✓</span>
          {{ success }}
        </div>

        <!-- 提交按鈕 -->
        <BaseButton
          type="submit"
          variant="primary"
          size="large"
          :loading="loading"
          :disabled="!form.role"
        >
          {{ loading ? '註冊中...' : '立即註冊' }}
        </BaseButton>

        <div class="link-container">
          <span>已有帳號？</span>
          <router-link to="/login" class="link">立即登入</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseInput from '@/components/common/BaseInput.vue'
import BaseButton from '@/components/common/BaseButton.vue'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  role: '',
  username: '',
  password: '',
  confirmPassword: '',
  displayName: '',
  email: '',
  phone: '',
  businessName: '',
  businessType: '',
  address: ''
})

const loading = ref(false)
const error = ref('')
const success = ref('')
const errors = ref({
  username: '',
  password: '',
  confirmPassword: '',
  businessName: ''
})

const selectRole = (role) => {
  form.value.role = role
  // 清除錯誤訊息
  error.value = ''
}

const validateForm = () => {
  errors.value = {
    username: '',
    password: '',
    confirmPassword: '',
    businessName: ''
  }

  let isValid = true

  // 驗證使用者名稱
  if (form.value.username.length < 4) {
    errors.value.username = '使用者名稱至少需要 4 個字元'
    isValid = false
  }

  // 驗證密碼
  if (form.value.password.length < 6) {
    errors.value.password = '密碼至少需要 6 個字元'
    isValid = false
  }

  // 驗證確認密碼
  if (form.value.password !== form.value.confirmPassword) {
    errors.value.confirmPassword = '兩次密碼輸入不一致'
    isValid = false
  }

  // 驗證商家名稱（如果是商家）
  if (form.value.role === 'merchant' && !form.value.businessName) {
    errors.value.businessName = '請輸入商家名稱'
    isValid = false
  }

  return isValid
}

const handleRegister = async () => {
  error.value = ''
  success.value = ''

  // 驗證角色選擇
  if (!form.value.role) {
    error.value = '請選擇您的身分（顧客或商家）'
    return
  }

  // 驗證表單
  if (!validateForm()) {
    return
  }

  loading.value = true

  // 準備額外資料
  const additionalData = {
    display_name: form.value.displayName,
    email: form.value.email,
    phone: form.value.phone
  }

  // 如果是商家，添加商家資訊
  if (form.value.role === 'merchant') {
    additionalData.business_name = form.value.businessName
    additionalData.business_type = form.value.businessType
    additionalData.address = form.value.address
  }

  const result = await authStore.register(
    form.value.username,
    form.value.password,
    form.value.confirmPassword,
    form.value.role,
    additionalData
  )

  if (result.success) {
    success.value = '註冊成功！正在跳轉到登入頁面...'
    setTimeout(() => {
      router.push('/login')
    }, 1500)
  } else {
    error.value = result.error
  }

  loading.value = false
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.register-card {
  background: white;
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 600px;
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

/* 角色選擇器 */
.role-selector {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 10px;
}

.role-card {
  padding: 20px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background: white;
}

.role-card:hover {
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.role-card.active {
  border-color: #667eea;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.role-icon {
  font-size: 40px;
  margin-bottom: 10px;
}

.role-name {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 5px;
}

.role-desc {
  font-size: 13px;
  opacity: 0.8;
}

/* 商家欄位區塊 */
.merchant-fields {
  padding: 20px;
  background: #f8f9ff;
  border-radius: 12px;
  border: 2px dashed #667eea;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #667eea;
  margin-bottom: 15px;
}

.section-title .icon {
  font-size: 20px;
}

/* 訊息樣式 */
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

.success-message {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #27ae60;
  font-size: 14px;
  padding: 12px 16px;
  background: #efe;
  border-radius: 8px;
  border: 1px solid #cfc;
}

.success-icon {
  font-size: 18px;
  font-weight: bold;
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
  .register-card {
    padding: 30px 20px;
  }

  .title {
    font-size: 26px;
  }

  .role-selector {
    grid-template-columns: 1fr;
  }

  .role-card {
    padding: 15px;
  }

  .role-icon {
    font-size: 32px;
  }
}
</style>
