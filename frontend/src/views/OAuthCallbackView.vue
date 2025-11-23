<template>
  <div class="oauth-callback-container">
    <div class="oauth-callback-card">
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>正在處理登入...</p>
      </div>
      <div v-else-if="error" class="error">
        <h2>登入失敗</h2>
        <p>{{ error }}</p>
        <router-link to="/login" class="button">返回登入頁面</router-link>
      </div>
      <div v-else class="success">
        <h2>登入成功！</h2>
        <p>正在跳轉...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    // 檢查是否有錯誤
    if (route.query.error) {
      try {
        // 嘗試解碼錯誤訊息，如果失敗則使用原始值
        error.value = decodeURIComponent(route.query.error)
      } catch (e) {
        // 如果解碼失敗，使用原始錯誤訊息或顯示通用錯誤
        error.value = route.query.error || '登入過程中發生錯誤'
      }
      loading.value = false
      return
    }

    const token = route.query.token
    const user = route.query.user
    const provider = route.query.provider

    if (!token) {
      error.value = '未收到登入憑證，請重試'
      loading.value = false
      return
    }

    // 解碼用戶名（如果有的話）
    let decodedUser = ''
    if (user) {
      try {
        decodedUser = decodeURIComponent(user)
      } catch (e) {
        decodedUser = user
      }
    }

    // 保存 token 和用戶資訊
    authStore.setAuth(token, { username: decodedUser })

    // 等待一下讓用戶看到成功訊息
    setTimeout(() => {
      router.push('/')
    }, 1000)
  } catch (err) {
    error.value = '處理登入時發生錯誤：' + (err.message || '未知錯誤')
    loading.value = false
  }
})
</script>

<style scoped>
.oauth-callback-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.oauth-callback-card {
  background: white;
  border-radius: 12px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading p {
  color: #666;
  font-size: 16px;
}

.error h2 {
  color: #e74c3c;
  margin-bottom: 15px;
}

.error p {
  color: #666;
  margin-bottom: 20px;
}

.success h2 {
  color: #27ae60;
  margin-bottom: 15px;
}

.success p {
  color: #666;
}

.button {
  display: inline-block;
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: opacity 0.3s;
}

.button:hover {
  opacity: 0.9;
}
</style>

