<template>
  <div class="dashboard">
    <div class="welcome-section">
      <h2 class="welcome-title">歡迎回來，{{ username }}！</h2>
      <p class="welcome-subtitle">這是您的儀表板概覽</p>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-content">
          <div class="stat-value">1,234</div>
          <div class="stat-label">總用戶數</div>
        </div>
        <div class="stat-trend positive">+12%</div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <div class="stat-value">5,678</div>
          <div class="stat-label">活躍會話</div>
        </div>
        <div class="stat-trend positive">+8%</div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">🔐</div>
        <div class="stat-content">
          <div class="stat-value">98.5%</div>
          <div class="stat-label">安全評分</div>
        </div>
        <div class="stat-trend positive">+2%</div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">⚡</div>
        <div class="stat-content">
          <div class="stat-value">234ms</div>
          <div class="stat-label">平均響應時間</div>
        </div>
        <div class="stat-trend negative">-5%</div>
      </div>
    </div>

    <div class="content-grid">
      <div class="card recent-activity">
        <h3 class="card-title">最近活動</h3>
        <div class="activity-list">
          <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
            <div class="activity-icon">{{ activity.icon }}</div>
            <div class="activity-content">
              <div class="activity-title">{{ activity.title }}</div>
              <div class="activity-time">{{ activity.time }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="card quick-actions">
        <h3 class="card-title">快速操作</h3>
        <div class="actions-grid">
          <button class="action-btn">
            <span class="action-icon">👤</span>
            <span class="action-text">編輯個人資料</span>
          </button>
          <button class="action-btn">
            <span class="action-icon">🔑</span>
            <span class="action-text">變更密碼</span>
          </button>
          <button class="action-btn">
            <span class="action-icon">🔗</span>
            <span class="action-text">綁定帳號</span>
          </button>
          <button class="action-btn">
            <span class="action-icon">📧</span>
            <span class="action-text">通知設定</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const username = computed(() => {
  return authStore.user?.username || '訪客'
})

const recentActivities = ref([
  { id: 1, icon: '🔐', title: '成功登入系統', time: '5 分鐘前' },
  { id: 2, icon: '👤', title: '更新個人資料', time: '2 小時前' },
  { id: 3, icon: '🔑', title: '變更密碼', time: '1 天前' },
  { id: 4, icon: '🔗', title: '綁定 Google 帳號', time: '3 天前' },
  { id: 5, icon: '📧', title: '驗證電子郵件', time: '1 週前' }
])
</script>

<style scoped>
.dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

.welcome-section {
  margin-bottom: 30px;
}

.welcome-title {
  font-size: 32px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.welcome-subtitle {
  font-size: 16px;
  color: #7f8c8d;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  font-size: 40px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #7f8c8d;
}

.stat-trend {
  font-size: 14px;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 6px;
}

.stat-trend.positive {
  color: #27ae60;
  background: #d5f4e6;
}

.stat-trend.negative {
  color: #e74c3c;
  background: #fadbd8;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 20px 0;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  transition: background 0.2s;
}

.activity-item:hover {
  background: #f8f9fa;
}

.activity-icon {
  font-size: 24px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f0f0;
  border-radius: 8px;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 4px;
}

.activity-time {
  font-size: 12px;
  color: #95a5a6;
}

.actions-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border: 2px solid transparent;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.action-btn:hover {
  background: white;
  border-color: #667eea;
  transform: translateX(4px);
}

.action-icon {
  font-size: 24px;
}

.action-text {
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
}

/* Responsive */
@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .welcome-title {
    font-size: 24px;
  }
}
</style>
