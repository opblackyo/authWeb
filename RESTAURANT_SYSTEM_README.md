# 餐廳訂餐系統 - 身分分流架構

## 系統概述

這是一個基於 **身分分流** 的餐廳訂餐平台，支援兩種用戶角色：
- **顧客（Customer）**：瀏覽餐廳、查看菜單、下訂單
- **商家（Merchant）**：管理菜單、接收訂單、處理訂單

系統採用 **Vue 3 + Flask** 前後端分離架構，實現了完整的身分驗證和角色權限控制。

## 核心功能

### 🔐 身分驗證系統
- ✅ 註冊時選擇角色（顧客/商家）
- ✅ 登入後根據角色自動分流
- ✅ JWT Token 認證
- ✅ OAuth 登入（LINE、Google）
- ✅ 帳號鎖定機制（防暴力破解）

### 👥 顧客功能
- ✅ 瀏覽餐廳列表
- ✅ 查看餐廳菜單
- ✅ 加入購物車
- ✅ 下訂單
- ✅ 查看訂單歷史
- ✅ 訂單狀態追蹤

### 🏪 商家功能
- ✅ 接單看板（Dashboard）
- ✅ 訂單管理（接單、準備中、完成）
- ✅ 菜單管理（新增、編輯、刪除）
- ✅ 商家資料管理
- ✅ 營業統計報表

## 技術架構

### 前端技術棧
- **Vue 3** - 使用 Composition API
- **Vue Router** - 路由管理和角色守衛
- **Pinia** - 狀態管理
- **Axios** - HTTP 請求
- **Vite** - 建置工具

### 後端技術棧
- **Python Flask** - Web 框架
- **Flask-JWT-Extended** - JWT 認證
- **MySQL** - 資料庫
- **PyMySQL** - 資料庫連接
- **Flask-CORS** - 跨域支援

### 共用元件庫
- **BaseButton** - 統一的按鈕組件（支援多種樣式和狀態）
- **BaseInput** - 統一的輸入框組件（支援驗證和圖標）
- **BaseCard** - 統一的卡片組件（支援多種變體）
- **BaseSelect** - 統一的下拉選單組件

## 資料庫結構

### 核心資料表

#### users（用戶表）
```sql
- id: 用戶 ID
- username: 用戶名
- role: 角色（customer/merchant）
- password: 密碼（加密）
- display_name: 顯示名稱
- email: 電子郵件
- phone: 電話號碼
- line_id: LINE ID（OAuth）
- google_id: Google ID（OAuth）
- created_at: 創建時間
```

#### merchants（商家表）
```sql
- id: 商家 ID
- user_id: 關聯的用戶 ID
- business_name: 商家名稱
- business_type: 商家類型
- address: 地址
- description: 描述
- logo_url: Logo 圖片
- is_verified: 是否已驗證
- rating: 評分
```

#### menu_items（菜單項目表）
```sql
- id: 菜品 ID
- merchant_id: 商家 ID
- name: 菜品名稱
- description: 描述
- price: 價格
- category: 分類
- image_url: 圖片
- is_available: 是否可用
```

#### orders（訂單表）
```sql
- id: 訂單 ID
- customer_id: 顧客 ID
- merchant_id: 商家 ID
- order_number: 訂單編號
- status: 訂單狀態（pending/confirmed/preparing/ready/completed/cancelled）
- total_amount: 總金額
- note: 備註
- created_at: 創建時間
```

#### order_items（訂單項目表）
```sql
- id: 項目 ID
- order_id: 訂單 ID
- menu_item_id: 菜品 ID
- quantity: 數量
- price: 單價
- subtotal: 小計
```

## 安裝與設定

### 1. 資料庫設定

執行資料庫遷移腳本：

```bash
# 在 MySQL 中執行
mysql -u root -p vue_auth < backend/migrations/add_user_role.sql
```

或在 phpMyAdmin 中直接執行 `backend/migrations/add_user_role.sql` 文件。

### 2. 後端設定

```bash
cd backend
pip install -r requirements.txt

# 設定環境變數（複製 env.example 為 .env）
cp env.example .env

# 編輯 .env 文件，設定資料庫和 JWT 密鑰
# 啟動後端
python app.py
```

### 3. 前端設定

```bash
cd frontend
npm install
npm run dev
```

## 使用流程

### 顧客流程

1. **註冊/登入**
   - 選擇「顧客」角色註冊
   - 或使用 OAuth 登入（自動設為顧客）

2. **瀏覽餐廳**
   - 登入後自動導向餐廳首頁
   - 瀏覽餐廳列表
   - 查看餐廳詳情和菜單

3. **下訂單**
   - 選擇菜品加入購物車
   - 確認訂單並提交
   - 查看訂單狀態

4. **訂單管理**
   - 查看訂單歷史
   - 追蹤訂單狀態
   - 評價訂單

### 商家流程

1. **註冊/登入**
   - 選擇「商家」角色註冊
   - 填寫商家資訊

2. **接單看板**
   - 登入後自動導向接單看板
   - 查看待處理訂單
   - 接受/拒絕訂單

3. **訂單處理**
   - 更新訂單狀態（準備中、已完成）
   - 查看訂單詳情
   - 訂單歷史記錄

4. **菜單管理**
   - 新增/編輯/刪除菜品
   - 設定菜品分類
   - 上傳菜品圖片
   - 設定菜品可用性

5. **商家管理**
   - 編輯商家資訊
   - 查看營業統計
   - 管理商家設定

## 路由結構

### 公開路由
- `/login` - 登入頁面
- `/register` - 註冊頁面
- `/oauth/callback` - OAuth 回調頁面

### 顧客路由（需要 customer 角色）
- `/restaurant` - 餐廳首頁
- `/restaurant/:id` - 餐廳詳情
- `/cart` - 購物車
- `/orders` - 我的訂單
- `/profile` - 個人資料

### 商家路由（需要 merchant 角色）
- `/merchant/dashboard` - 接單看板
- `/merchant/orders` - 訂單管理
- `/merchant/menu` - 菜單管理
- `/merchant/profile` - 商家資料
- `/merchant/settings` - 商家設定

## API 端點

### 認證 API
- `POST /api/register` - 註冊（支援角色選擇）
- `POST /api/login` - 登入（返回角色資訊）
- `GET /api/profile` - 獲取個人資料（包含角色和商家資訊）

### 商家 API
- `GET /api/merchants` - 獲取商家列表
- `GET /api/merchants/:id` - 獲取商家詳情
- `PUT /api/merchants/:id` - 更新商家資訊
- `GET /api/merchants/:id/menu` - 獲取商家菜單

### 菜單 API
- `GET /api/menu-items` - 獲取菜單項目
- `POST /api/menu-items` - 新增菜單項目
- `PUT /api/menu-items/:id` - 更新菜單項目
- `DELETE /api/menu-items/:id` - 刪除菜單項目

### 訂單 API
- `GET /api/orders` - 獲取訂單列表（根據角色返回不同數據）
- `POST /api/orders` - 創建訂單
- `GET /api/orders/:id` - 獲取訂單詳情
- `PUT /api/orders/:id/status` - 更新訂單狀態

## 下一步開發計劃

- [ ] 實作顧客餐廳首頁
- [ ] 實作商家接單看板
- [ ] 實作菜單管理功能
- [ ] 實作訂單系統
- [ ] 實作購物車功能
- [ ] 實作即時通知（WebSocket）
- [ ] 實作圖片上傳功能
- [ ] 實作評分和評論系統
- [ ] 實作營業統計報表
- [ ] 實作支付整合

## 授權

MIT License

