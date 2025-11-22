import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// 全域錯誤處理
app.config.errorHandler = (err, vm, info) => {
  console.error('全域錯誤:', err, info)
}

app.mount('#app')

