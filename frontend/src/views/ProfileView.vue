<template>
  <div class="profile-view">
    <div class="profile-header">
      <h2 class="page-title">個人資料</h2>
      <p class="page-subtitle">管理您的個人資訊</p>
    </div>

    <div class="profile-content">
      <div class="profile-card">
        <div class="profile-avatar-section">
          <div class="avatar-large">{{ userInitial }}</div>
          <button class="change-avatar-btn">更換頭像</button>
        </div>

        <div class="profile-info">
          <div class="info-group">
            <label class="info-label">使用者名稱</label>
            <div class="info-value">{{ user?.username || '未設定' }}</div>
          </div>

          <div class="info-group">
            <label class="info-label">電子郵件</label>
            <div class="info-value">{{ user?.email || '未設定' }}</div>
          </div>

          <div class="info-group">
            <label class="info-label">顯示名稱</label>
            <div class="info-value">{{ user?.display_name || '未設定' }}</div>
          </div>

          <div class="info-group">
            <label class="info-label">帳號狀態</label>
            <div class="info-value">
              <span class="status-badge active">已啟用</span>
            </div>
          </div>

          <div class="info-group">
            <label class="info-label">綁定帳號</label>
            <div class="linked-accounts">
              <div class="linked-item" :class="{ linked: user?.is_line_linked }">
                <span class="linked-icon">📱</span>
                <span class="linked-text">LINE</span>
                <span v-if="user?.is_line_linked" class="linked-status">已綁定</span>
                <span v-else class="linked-status">未綁定</span>
              </div>
              <div class="linked-item" :class="{ linked: user?.is_google_linked }">
                <span class="linked-icon">🔍</span>
                <span class="linked-text">Google</span>
                <span v-if="user?.is_google_linked" class="linked-status">已綁定</span>
                <span v-else class="linked-status">未綁定</span>
              </div>
            </div>
          </div>

          <div class="action-buttons">
            <button class="btn btn-primary">編輯資料</button>
            <button class="btn btn-secondary">變更密碼</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const user = ref(null)

const userInitial = computed(() => {
  return user.value?.username?.charAt(0).toUpperCase() || 'U'
})

onMounted(async () => {
  const result = await authStore.fetchProfile()
  if (result.success) {
    user.value = authStore.user
  }
})
</script>

<style scoped>
.profile-view {
  max-width: 900px;
  margin: 0 auto;
}

.profile-header {
  margin-bottom: 30px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.page-subtitle {
  font-size: 14px;
  color: #7f8c8d;
  margin: 0;
}

.profile-card {
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.profile-avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 40px;
  padding-bottom: 30px;
  border-bottom: 1px solid #e0e0e0;
}

.avatar-large {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  font-weight: 600;
  margin-bottom: 20px;
}

.change-avatar-btn {
  padding: 10px 24px;
  background: #f8f9fa;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
  transition: all 0.2s;
}

.change-avatar-btn:hover {
  background: white;
  border-color: #667eea;
}

.profile-info {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.info-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-label {
  font-size: 14px;
  font-weight: 600;
  color: #7f8c8d;
}

.info-value {
  font-size: 16px;
  color: #2c3e50;
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.active {
  background: #d5f4e6;
  color: #27ae60;
}

.linked-accounts {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.linked-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 2px solid transparent;
}

.linked-item.linked {
  border-color: #27ae60;
  background: #d5f4e6;
}

.linked-icon {
  font-size: 24px;
}

.linked-text {
  flex: 1;
  font-weight: 500;
  color: #2c3e50;
}

.linked-status {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 4px;
  background: white;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: #f8f9fa;
  color: #2c3e50;
  border: 2px solid #e0e0e0;
}

.btn-secondary:hover {
  background: white;
  border-color: #667eea;
}
</style>
