<template>
  <div class="dashboard-layout">
    <Sidebar />
    <div class="main-content" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <Header />
      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import Header from '@/components/Header.vue'

const isSidebarCollapsed = ref(false)
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  min-height: 100vh;
  background: #f5f7fa;
}

.main-content {
  flex: 1;
  margin-left: 260px;
  transition: margin-left 0.3s ease;
  display: flex;
  flex-direction: column;
}

.main-content.sidebar-collapsed {
  margin-left: 80px;
}

.content {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
}

/* Responsive */
@media (max-width: 768px) {
  .main-content {
    margin-left: 80px;
  }
  
  .main-content.sidebar-collapsed {
    margin-left: 0;
  }
}
</style>

