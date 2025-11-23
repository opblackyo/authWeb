<template>
  <div class="register-container">
    <div class="register-card">
      <h1 class="title">註冊</h1>
      <form @submit.prevent="handleRegister" class="form">
        <div class="form-group">
          <label for="username">使用者名稱</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            placeholder="請輸入使用者名稱（至少 4 個字元）"
            class="input"
            minlength="4"
          />
        </div>
        <div class="form-group">
          <label for="password">密碼</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            placeholder="請輸入密碼（至少 6 個字元）"
            class="input"
            minlength="6"
          />
        </div>
        <div class="form-group">
          <label for="confirmPassword">確認密碼</label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            required
            placeholder="請再次輸入密碼"
            class="input"
            minlength="6"
          />
        </div>
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        <div v-if="success" class="success-message">
          {{ success }}
        </div>
        <button type="submit" :disabled="loading" class="submit-button">
          {{ loading ? '註冊中...' : '註冊' }}
        </button>
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

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)
const error = ref('')
const success = ref('')

const handleRegister = async () => {
  error.value = ''
  success.value = ''
  
  if (form.value.password !== form.value.confirmPassword) {
    error.value = '兩次密碼輸入不一致'
    return
  }
  
  loading.value = true

  const result = await authStore.register(
    form.value.username,
    form.value.password,
    form.value.confirmPassword
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
}

.register-card {
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

.error-message {
  color: #e74c3c;
  font-size: 14px;
  padding: 10px;
  background: #fee;
  border-radius: 6px;
  border: 1px solid #fcc;
}

.success-message {
  color: #27ae60;
  font-size: 14px;
  padding: 10px;
  background: #efe;
  border-radius: 6px;
  border: 1px solid #cfc;
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
