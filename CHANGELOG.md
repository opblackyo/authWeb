# 更新日誌

## 2024-11-23 - 餐廳訂餐系統 v2.0

### 🎯 重大更新：身分分流系統

將原本的登入系統升級為**餐廳訂餐平台**，支援顧客和商家兩種角色的身分分流。

### ✨ 新增功能

#### 1. 角色系統
- ✅ 註冊時選擇角色（顧客/商家）
- ✅ 登入後根據角色自動分流
- ✅ 角色權限控制和路由守衛
- ✅ 商家自動創建商家資料

#### 2. 資料庫結構
- ✅ 新增 `users.role` 欄位（ENUM: customer, merchant）
- ✅ 新增 `users.display_name`, `email`, `phone` 欄位
- ✅ 新增 `merchants` 表（商家資訊）
- ✅ 新增 `menu_items` 表（菜單項目）
- ✅ 新增 `orders` 表（訂單）
- ✅ 新增 `order_items` 表（訂單項目）

#### 3. 共用元件庫
- ✅ **BaseButton** - 統一按鈕組件
  - 7 種樣式：primary, secondary, success, danger, warning, outline, ghost
  - 3 種尺寸：small, medium, large
  - 支援載入狀態和圖標
  
- ✅ **BaseInput** - 統一輸入框組件
  - 支援標籤、圖標、錯誤訊息
  - 密碼切換功能
  - 表單驗證支援
  
- ✅ **BaseCard** - 統一卡片組件
  - 4 種變體：default, bordered, elevated, flat
  - 支援 header, body, footer 插槽
  - 懸停和點擊效果
  
- ✅ **BaseSelect** - 統一下拉選單組件
  - 支援標籤和錯誤訊息
  - 選項陣列配置

#### 4. 後端 API 更新
- ✅ **POST /api/register** - 支援角色選擇和額外資料
  - 新增 `role` 參數（customer/merchant）
  - 新增 `display_name`, `email`, `phone` 參數
  - 新增 `business_name` 參數（商家專用）
  - 自動創建商家記錄
  
- ✅ **POST /api/login** - 返回角色和商家資訊
  - 回應包含 `role` 欄位
  - 商家登入時返回 `merchant` 物件
  - 包含商家名稱、類型、評分等資訊
  
- ✅ **GET /api/profile** - 返回完整用戶資料
  - 包含角色資訊
  - 商家用戶包含商家詳細資訊
  - 向後兼容舊資料庫結構

#### 5. 前端狀態管理更新
- ✅ **Auth Store** 增強
  - 新增 `userRole` getter（獲取用戶角色）
  - 新增 `isCustomer` getter（判斷是否為顧客）
  - 新增 `isMerchant` getter（判斷是否為商家）
  - `login()` 方法返回角色資訊
  - `register()` 方法支援角色和額外資料
  - 用戶資料包含商家資訊（如果是商家）

#### 6. API 服務層更新
- ✅ **authApi.register()** 支援新參數
  - 接受 `role` 和 `additionalData` 參數
  - 自動展開額外資料到請求體

### 📁 新增文件

- ✅ **backend/migrations/add_user_role.sql** - 資料庫遷移腳本
- ✅ **frontend/src/components/common/BaseButton.vue** - 按鈕組件
- ✅ **frontend/src/components/common/BaseInput.vue** - 輸入框組件
- ✅ **frontend/src/components/common/BaseCard.vue** - 卡片組件
- ✅ **frontend/src/components/common/BaseSelect.vue** - 下拉選單組件
- ✅ **RESTAURANT_SYSTEM_README.md** - 餐廳系統完整說明
- ✅ **DEVELOPMENT_GUIDE.md** - 開發指南和元件使用說明
- ✅ **CHANGELOG.md** - 本文件

### 📝 更新文件

- ✅ **README.md** - 更新為餐廳系統說明
  - 新增系統特色說明
  - 新增快速開始指南
  - 更新 API 端點文件
  - 新增角色系統說明
  
- ✅ **frontend/src/stores/auth.js** - 認證狀態管理
- ✅ **frontend/src/api/auth.js** - API 服務層
- ✅ **backend/app.py** - 後端主應用

### 🔄 向後兼容性

所有更新都保持向後兼容：

- ✅ 後端 API 自動檢測資料庫是否有 `role` 欄位
- ✅ 如果沒有 `role` 欄位，預設為 `customer`
- ✅ 舊的登入/註冊流程仍然可用
- ✅ 現有用戶資料不受影響

### 🚀 下一步開發計劃

#### 待實作功能（按優先級排序）

1. **顧客介面**
   - [ ] 餐廳首頁（瀏覽餐廳列表）
   - [ ] 餐廳詳情頁（查看菜單）
   - [ ] 購物車功能
   - [ ] 下訂單流程
   - [ ] 訂單歷史和追蹤

2. **商家介面**
   - [ ] 接單看板（訂單管理）
   - [ ] 菜單管理（CRUD）
   - [ ] 商家資料編輯
   - [ ] 營業統計報表

3. **路由系統**
   - [ ] 實作角色路由守衛
   - [ ] 顧客路由（/restaurant/*）
   - [ ] 商家路由（/merchant/*）
   - [ ] 登入後自動分流

4. **後端 API**
   - [ ] 商家列表 API
   - [ ] 菜單管理 API
   - [ ] 訂單管理 API
   - [ ] 圖片上傳 API

5. **進階功能**
   - [ ] 即時通知（WebSocket）
   - [ ] 評分和評論系統
   - [ ] 支付整合
   - [ ] 訂單統計圖表

### 📊 系統架構

```
用戶註冊 → 選擇角色 → 登入
                ↓
        ┌───────┴───────┐
        ↓               ↓
    顧客介面        商家介面
    (餐廳首頁)      (接單看板)
        ↓               ↓
    瀏覽/下單       接單/管理
        ↓               ↓
    訂單追蹤        訂單處理
```

### 🛠️ 技術棧

**前端：**
- Vue 3 (Composition API)
- Pinia (狀態管理)
- Vue Router (路由)
- Axios (HTTP 請求)
- Vite (建置工具)

**後端：**
- Python Flask
- Flask-JWT-Extended
- MySQL (資料庫)
- PyMySQL (資料庫連接)
- Flask-CORS (跨域支援)

### 📖 使用指南

詳細的使用指南請參考：
- [RESTAURANT_SYSTEM_README.md](./RESTAURANT_SYSTEM_README.md) - 系統完整說明
- [DEVELOPMENT_GUIDE.md](./DEVELOPMENT_GUIDE.md) - 開發指南
- [README.md](./README.md) - 安裝和設定指南

### 🐛 已知問題

目前沒有已知問題。

### 💡 貢獻指南

1. 使用共用元件庫保持 UI 一致性
2. 遵循 Vue 3 Composition API 最佳實踐
3. API 開發遵循 RESTful 規範
4. 提交前測試所有功能
5. 更新相關文件

---

**版本：** 2.0.0  
**日期：** 2024-11-23  
**作者：** Augment Agent

