# Dashboard 框架快速開始指南

## 🎉 已完成的功能

### ✅ 核心組件
- **Sidebar（側邊欄）** - 可折疊的導航側邊欄
- **Header（頂部欄）** - 包含搜尋、通知、用戶選單
- **DashboardLayout（佈局）** - 整合 Sidebar 和 Header 的主佈局

### ✅ 頁面視圖
- **DashboardView** - 儀表板首頁（統計卡片、活動列表、快速操作）
- **ProfileView** - 個人資料頁面（頭像、資訊、綁定帳號）
- **SettingsView** - 設定頁面（通知、隱私、安全設定）

### ✅ 路由配置
- 已更新路由使用 Dashboard 佈局
- 所有認證頁面自動顯示 Sidebar 和 Header
- 登入後自動導向 `/dashboard`

## 📁 檔案結構

```
frontend/src/
├── components/
│   ├── Sidebar.vue          # 側邊欄組件
│   └── Header.vue           # 頂部欄組件
├── layouts/
│   └── DashboardLayout.vue  # Dashboard 佈局
├── views/
│   ├── DashboardView.vue    # 儀表板頁面
│   ├── ProfileView.vue      # 個人資料頁面
│   ├── SettingsView.vue     # 設定頁面
│   ├── LoginView.vue        # 登入頁面（已存在）
│   ├── RegisterView.vue     # 註冊頁面（已存在）
│   └── HomeView.vue         # 舊首頁（保留）
└── router/
    └── index.js             # 路由配置（已更新）
```

## 🚀 如何啟動

### 1. 確保後端運行中

```bash
cd backend
python app.py
```

### 2. 啟動前端開發伺服器

```bash
cd frontend
npm run dev
```

### 3. 訪問應用

打開瀏覽器訪問：`http://localhost:5173`

## 🎨 功能展示

### Sidebar（側邊欄）
- **可折疊設計**：點擊切換按鈕可展開/收起
- **導航菜單**：
  - 📊 儀表板
  - 👤 個人資料
  - ⚙️ 設定
  - 🔑 帳號管理
- **用戶資訊**：底部顯示當前用戶頭像和名稱
- **響應式**：手機版自動折疊

### Header（頂部欄）
- **動態標題**：根據當前頁面顯示標題
- **搜尋框**：可擴展的搜尋輸入框
- **通知中心**：顯示未讀通知數量
- **用戶選單**：
  - 個人資料
  - 設定
  - 登出

### DashboardView（儀表板）
- **統計卡片**：4 個統計數據卡片
  - 總用戶數
  - 活躍會話
  - 安全評分
  - 平均響應時間
- **最近活動**：時間軸式活動列表
- **快速操作**：常用功能快捷按鈕

### ProfileView（個人資料）
- **大型頭像**：顯示用戶首字母
- **個人資訊**：用戶名、郵箱、顯示名稱
- **帳號狀態**：顯示帳號啟用狀態
- **綁定帳號**：LINE 和 Google 綁定狀態
- **操作按鈕**：編輯資料、變更密碼

### SettingsView（設定）
- **通知設定**：
  - 電子郵件通知
  - 推送通知
  - 安全警報
- **隱私設定**：
  - 個人資料公開
  - 活動狀態顯示
- **安全設定**：
  - 雙因素驗證
  - 登入裝置管理

## 🎯 使用流程

1. **登入系統** → 自動導向 `/dashboard`
2. **查看儀表板** → 統計數據和最近活動
3. **點擊側邊欄** → 切換到不同頁面
4. **個人資料** → 查看和編輯個人資訊
5. **設定** → 調整偏好設定
6. **登出** → 點擊 Header 用戶選單中的登出

## 🎨 自訂指南

### 修改側邊欄菜單

編輯 `frontend/src/components/Sidebar.vue`：

```javascript
const menuItems = [
  { path: '/dashboard', label: '儀表板', icon: '📊' },
  { path: '/profile', label: '個人資料', icon: '👤' },
  { path: '/settings', label: '設定', icon: '⚙️' },
  { path: '/account', label: '帳號管理', icon: '🔑' },
  // 添加新的菜單項目
  { path: '/reports', label: '報表', icon: '📈' }
]
```

### 修改色彩方案

主要色彩定義在各組件的 `<style>` 區塊中：

- **主色調**：`#667eea` → `#764ba2`
- **側邊欄**：`#2c3e50` → `#34495e`
- **成功色**：`#27ae60`
- **警告色**：`#e74c3c`

### 添加新頁面

1. 在 `frontend/src/views/` 創建新的 Vue 組件
2. 在 `frontend/src/router/index.js` 添加路由
3. 在 Sidebar 添加菜單項目

## 📱 響應式設計

- **桌面版**（> 768px）：Sidebar 寬度 260px
- **平板/手機**（≤ 768px）：Sidebar 寬度 80px（折疊）

## 🔧 技術棧

- **Vue 3** - 前端框架
- **Vue Router** - 路由管理
- **Pinia** - 狀態管理
- **Vite** - 建置工具

## 📝 注意事項

1. 所有需要認證的頁面都會自動使用 Dashboard 佈局
2. 登入/註冊頁面不使用 Dashboard 佈局
3. 路由守衛會自動處理認證檢查
4. 用戶資訊從 Pinia store 中獲取

## 🚀 下一步建議

1. **實作搜尋功能** - 連接後端 API
2. **實作通知系統** - 即時通知推送
3. **添加圖表** - 使用 Chart.js 或 ECharts
4. **實作設定儲存** - 連接後端 API
5. **添加深色模式** - 主題切換功能
6. **完善個人資料編輯** - 表單驗證和提交
7. **添加更多頁面** - 如報表、日誌等

## 📚 相關文件

- 詳細說明：`frontend/DASHBOARD_README.md`
- 主專案說明：`README.md`

## 💡 提示

- 使用 Vue DevTools 可以更好地調試組件
- 所有組件都支援響應式設計
- 可以通過修改 CSS 變數來快速調整樣式
- 建議使用 ESLint 保持代碼品質

---

**祝您使用愉快！** 🎉

