<template>
  <div class="home-container">
    <div class="home-card">
      <h1 class="welcome-title">歡迎回來！</h1>
      <div v-if="loading" class="loading">載入中...</div>
      <div v-else-if="user" class="user-info">
        <div class="info-item">
          <span class="label">用戶名：</span>
          <span class="value">{{ user.username }}</span>
        </div>
        <div class="info-item">
          <span class="label">電子郵件：</span>
          <span class="value">{{ user.email }}</span>
        </div>
        <div class="info-item">
          <span class="label">註冊時間：</span>
          <span class="value">{{ formatDate(user.created_at) }}</span>
        </div>
        <button @click="handleLogout" class="logout-button">登出</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const user = ref(authStore.user)

const formatDate = (dateString) => {
  if (!dateString) return '未知'
  const date = new Date(dateString)
  return date.toLocaleString('zh-TW')
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }

  loading.value = true
  const result = await authStore.fetchProfile()
  if (result.success) {
    user.value = authStore.user
  }
  loading.value = false
})
</script>

<style scoped>
.home-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.home-card {
  background: white;
  border-radius: 12px;
  padding: 40px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.welcome-title {
  font-size: 32px;
  font-weight: 600;
  color: #333;
  margin-bottom: 30px;
  text-align: center;
}

.loading {
  text-align: center;
  color: #666;
  font-size: 16px;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-item {
  display: flex;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.label {
  font-weight: 600;
  color: #555;
  min-width: 100px;
}

.value {
  color: #333;
  flex: 1;
}

.logout-button {
  margin-top: 20px;
  padding: 14px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.3s;
}

.logout-button:hover {
  opacity: 0.9;
}
</style>

