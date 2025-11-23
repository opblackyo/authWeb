<template>
  <div class="settings-view">
    <div class="settings-header">
      <h2 class="page-title">設定</h2>
      <p class="page-subtitle">管理您的偏好設定</p>
    </div>

    <div class="settings-content">
      <div class="settings-card">
        <h3 class="section-title">通知設定</h3>
        <div class="settings-group">
          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-label">電子郵件通知</div>
              <div class="setting-description">接收重要更新和通知</div>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="settings.emailNotifications" />
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-label">推送通知</div>
              <div class="setting-description">在瀏覽器中接收即時通知</div>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="settings.pushNotifications" />
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-label">安全警報</div>
              <div class="setting-description">帳號安全相關的重要通知</div>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="settings.securityAlerts" />
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>
      </div>

      <div class="settings-card">
        <h3 class="section-title">隱私設定</h3>
        <div class="settings-group">
          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-label">個人資料公開</div>
              <div class="setting-description">允許其他用戶查看您的個人資料</div>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="settings.profilePublic" />
              <span class="toggle-slider"></span>
            </label>
          </div>

          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-label">活動狀態</div>
              <div class="setting-description">顯示您的線上狀態</div>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="settings.showOnlineStatus" />
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>
      </div>

      <div class="settings-card">
        <h3 class="section-title">安全設定</h3>
        <div class="settings-group">
          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-label">雙因素驗證</div>
              <div class="setting-description">為您的帳號增加額外的安全層</div>
            </div>
            <button class="btn btn-outline">啟用</button>
          </div>

          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-label">登入裝置管理</div>
              <div class="setting-description">查看和管理已登入的裝置</div>
            </div>
            <button class="btn btn-outline">管理</button>
          </div>
        </div>
      </div>

      <div class="settings-actions">
        <button class="btn btn-primary">儲存變更</button>
        <button class="btn btn-secondary">重設</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const settings = ref({
  emailNotifications: true,
  pushNotifications: false,
  securityAlerts: true,
  profilePublic: false,
  showOnlineStatus: true
})
</script>

<style scoped>
.settings-view {
  max-width: 900px;
  margin: 0 auto;
}

.settings-header {
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

.settings-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.settings-card {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 20px 0;
}

.settings-group {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.setting-info {
  flex: 1;
}

.setting-label {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 4px;
}

.setting-description {
  font-size: 14px;
  color: #7f8c8d;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 26px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.3s;
  border-radius: 26px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

input:checked + .toggle-slider:before {
  transform: translateX(24px);
}

.btn {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-outline {
  background: transparent;
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-outline:hover {
  background: #667eea;
  color: white;
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

.settings-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}
</style>
