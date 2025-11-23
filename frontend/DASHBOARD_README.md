# Dashboard 框架說明

## 概述

這是一個完整的 Dashboard 框架，包含 Sidebar（側邊欄）和 Header（頂部導航欄）組件，適用於需要後台管理介面的應用程式。

## 架構組成

### 1. 佈局組件 (Layouts)

#### `DashboardLayout.vue`
- 主要佈局容器
- 整合 Sidebar 和 Header 組件
- 提供響應式設計
- 位置：`frontend/src/layouts/DashboardLayout.vue`

### 2. 核心組件 (Components)

#### `Sidebar.vue`
- 左側導航欄
- 可折疊/展開功能
- 導航菜單項目
- 用戶資訊顯示
- 位置：`frontend/src/components/Sidebar.vue`

**功能特點：**
- 🎨 漸層背景設計
- 📱 響應式支援
- 🔄 平滑動畫過渡
- 👤 用戶頭像顯示
- 📍 當前路由高亮

**菜單項目：**
- 儀表板 (Dashboard)
- 個人資料 (Profile)
- 設定 (Settings)
- 帳號管理 (Account)

#### `Header.vue`
- 頂部導航欄
- 搜尋功能
- 通知中心
- 用戶下拉選單
- 位置：`frontend/src/components/Header.vue`

**功能特點：**
- 🔍 搜尋框
- 🔔 通知提醒（含未讀數量徽章）
- 👤 用戶選單（個人資料、設定、登出）
- 📄 動態頁面標題
- 🎯 點擊外部自動關閉下拉選單

### 3. 頁面視圖 (Views)

#### `DashboardView.vue`
- 儀表板首頁
- 統計卡片展示
- 最近活動列表
- 快速操作按鈕
- 位置：`frontend/src/views/DashboardView.vue`

**包含內容：**
- 📊 統計數據卡片（4個）
- 📝 最近活動時間軸
- ⚡ 快速操作面板

#### `ProfileView.vue`
- 個人資料頁面
- 用戶資訊展示
- 頭像管理
- 綁定帳號狀態
- 位置：`frontend/src/views/ProfileView.vue`

**功能：**
- 👤 大型用戶頭像
- 📋 個人資訊顯示
- 🔗 第三方帳號綁定狀態（LINE、Google）
- ✏️ 編輯資料按鈕
- 🔑 變更密碼按鈕

#### `SettingsView.vue`
- 設定頁面
- 通知偏好設定
- 隱私設定
- 安全設定
- 位置：`frontend/src/views/SettingsView.vue`

**設定項目：**
- 📧 通知設定（電子郵件、推送、安全警報）
- 🔒 隱私設定（個人資料公開、活動狀態）
- 🛡️ 安全設定（雙因素驗證、裝置管理）

## 路由配置

路由已更新為使用 Dashboard 佈局，所有需要認證的頁面都會顯示 Sidebar 和 Header。

```javascript
{
  path: '/',
  component: DashboardLayout,
  meta: { requiresAuth: true },
  children: [
    { path: 'dashboard', component: DashboardView },
    { path: 'profile', component: ProfileView },
    { path: 'settings', component: SettingsView },
    { path: 'account', component: HomeView }
  ]
}
```

## 樣式設計

### 色彩方案
- 主色調：`#667eea` → `#764ba2` (漸層)
- 側邊欄：`#2c3e50` → `#34495e` (深色漸層)
- 背景色：`#f5f7fa` (淺灰)
- 文字色：`#2c3e50` (深灰)
- 次要文字：`#7f8c8d` (中灰)

### 響應式斷點
- 桌面版：Sidebar 寬度 260px
- 平板/手機：Sidebar 寬度 80px（折疊狀態）
- 斷點：768px

## 使用方式

### 1. 啟動開發伺服器

```bash
cd frontend
npm run dev
```

### 2. 訪問頁面

- 登入後會自動導向：`http://localhost:5173/dashboard`
- 個人資料：`http://localhost:5173/profile`
- 設定：`http://localhost:5173/settings`

### 3. 自訂菜單項目

編輯 `Sidebar.vue` 中的 `menuItems` 陣列：

```javascript
const menuItems = [
  { path: '/dashboard', label: '儀表板', icon: '📊' },
  { path: '/profile', label: '個人資料', icon: '👤' },
  // 添加更多項目...
]
```

## 特色功能

✅ 完整的 Dashboard 框架
✅ 響應式設計（支援手機、平板、桌面）
✅ 可折疊側邊欄
✅ 用戶下拉選單
✅ 通知中心
✅ 搜尋功能
✅ 平滑動畫效果
✅ 現代化 UI 設計
✅ 易於擴展和自訂

## 後續擴展建議

1. 實作搜尋功能的後端 API
2. 實作通知系統
3. 添加更多統計圖表（使用 Chart.js 或 ECharts）
4. 實作設定頁面的儲存功能
5. 添加深色模式切換
6. 實作個人資料編輯功能
7. 添加更多頁面（如帳號管理、系統日誌等）

