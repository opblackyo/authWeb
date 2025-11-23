<template>
  <header class="header">
    <div class="header-left">
      <h1 class="page-title">{{ pageTitle }}</h1>
    </div>

    <div class="header-right">
      <div class="search-box">
        <input 
          type="text" 
          placeholder="搜尋..." 
          class="search-input"
          v-model="searchQuery"
        />
        <span class="search-icon">🔍</span>
      </div>

      <div class="notifications">
        <button class="notification-btn">
          <span class="notification-icon">🔔</span>
          <span v-if="notificationCount > 0" class="notification-badge">{{ notificationCount }}</span>
        </button>
      </div>

      <div class="user-menu">
        <button @click="toggleUserMenu" class="user-menu-btn">
          <div class="user-avatar">{{ userInitial }}</div>
          <span class="user-name">{{ username }}</span>
          <span class="dropdown-arrow">▼</span>
        </button>

        <div v-if="showUserMenu" class="user-dropdown">
          <router-link to="/profile" class="dropdown-item" @click="closeUserMenu">
            <span class="dropdown-icon">👤</span>
            個人資料
          </router-link>
          <router-link to="/settings" class="dropdown-item" @click="closeUserMenu">
            <span class="dropdown-icon">⚙️</span>
            設定
          </router-link>
          <div class="dropdown-divider"></div>
          <button @click="handleLogout" class="dropdown-item logout">
            <span class="dropdown-icon">🚪</span>
            登出
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const searchQuery = ref('')
const showUserMenu = ref(false)
const notificationCount = ref(3)

const pageTitle = computed(() => {
  const titles = {
    '/dashboard': '儀表板',
    '/profile': '個人資料',
    '/settings': '設定',
    '/account': '帳號管理'
  }
  return titles[route.path] || '首頁'
})

const username = computed(() => {
  return authStore.user?.username || '訪客'
})

const userInitial = computed(() => {
  return username.value.charAt(0).toUpperCase()
})

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const closeUserMenu = () => {
  showUserMenu.value = false
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  const userMenu = document.querySelector('.user-menu')
  if (userMenu && !userMenu.contains(event.target)) {
    closeUserMenu()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.header {
  height: 70px;
  background: white;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
  position: sticky;
  top: 0;
  z-index: 999;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.header-left {
  flex: 1;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.search-box {
  position: relative;
}

.search-input {
  padding: 10px 40px 10px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 25px;
  width: 250px;
  font-size: 14px;
  transition: all 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #3498db;
  width: 300px;
}

.search-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 16px;
  color: #999;
}

.notifications {
  position: relative;
}

.notification-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  position: relative;
  padding: 8px;
  border-radius: 50%;
  transition: background 0.2s;
}

.notification-btn:hover {
  background: #f5f5f5;
}

.notification-icon {
  font-size: 22px;
}

.notification-badge {
  position: absolute;
  top: 5px;
  right: 5px;
  background: #e74c3c;
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 10px;
  font-weight: 600;
}

.user-menu {
  position: relative;
}

.user-menu-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 25px;
  transition: background 0.2s;
}

.user-menu-btn:hover {
  background: #f5f5f5;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 16px;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
}

.dropdown-arrow {
  font-size: 10px;
  color: #999;
}

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 10px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 200px;
  overflow: hidden;
  z-index: 1000;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: #2c3e50;
  text-decoration: none;
  background: transparent;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  transition: background 0.2s;
  font-size: 14px;
}

.dropdown-item:hover {
  background: #f5f5f5;
}

.dropdown-item.logout {
  color: #e74c3c;
}

.dropdown-item.logout:hover {
  background: #fee;
}

.dropdown-icon {
  font-size: 16px;
}

.dropdown-divider {
  height: 1px;
  background: #e0e0e0;
  margin: 5px 0;
}
</style>
