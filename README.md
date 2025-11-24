# 餐廳訂餐系統

一個基於 **Flask + Vue 3** 的餐廳訂餐平台，支援**顧客**和**商家**兩種角色的身分分流系統。

## ✨ 核心功能

- 🔐 **身分驗證**：JWT + OAuth（LINE、Google）+ 帳號鎖定機制
- 👥 **顧客功能**：瀏覽餐廳、查看菜單、下訂單、訂單追蹤
- 🏪 **商家功能**：接單看板、訂單管理、菜單管理、營業統計
- 🎨 **共用元件庫**：統一的 UI 元件設計

## 📁 專案結構

```
authWeb/
├── backend/
│   ├── app.py                # Flask 主應用
│   ├── init_database.sql     # 資料庫初始化腳本
│   ├── requirements.txt      # Python 依賴
│   └── .env.example          # 環境變數範例
└── frontend/
    ├── src/
    │   ├── components/       # Vue 組件
    │   ├── views/            # 頁面視圖
    │   ├── stores/           # Pinia 狀態管理
    │   └── router/           # 路由配置
    └── package.json          # Node.js 依賴
```

## 🛠️ 技術棧

**後端**：Python 3 · Flask · Flask-JWT-Extended · MySQL · PyMySQL
**前端**：Vue 3 · Vue Router · Pinia · Axios · Vite

## 🚀 快速開始

### 1. 資料庫設定

啟動 XAMPP 的 MySQL 服務，然後執行：

```bash
# 創建資料庫
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS vue_auth CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 初始化資料表
mysql -u root -p vue_auth < backend/init_database.sql
```

或在 phpMyAdmin 中執行 `backend/init_database.sql`。

### 2. 後端設定

```bash
cd backend

# 建立虛擬環境（建議）
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 安裝依賴
pip install -r requirements.txt

# 設定環境變數
copy env.example .env  # Windows
# cp env.example .env  # Linux/Mac

# 編輯 .env 檔案，設定必要參數：
# JWT_SECRET_KEY=your-secret-key
# DB_PASSWORD=你的MySQL密碼

# 啟動後端
python app.py
```

後端運行於 `http://localhost:5000`

### 3. 前端設定

```bash
cd frontend

# 安裝依賴
npm install

# 啟動開發伺服器
npm run dev
```

前端運行於 `http://localhost:5173`

## 💡 使用說明

### 顧客流程
1. 註冊帳號並選擇「顧客」角色
2. 登入後瀏覽餐廳列表
3. 查看菜單並加入購物車
4. 下訂單並追蹤訂單狀態

### 商家流程
1. 註冊帳號並選擇「商家」角色，填寫商家名稱
2. 登入後進入接單看板
3. 管理菜單項目（新增、編輯、刪除）
4. 處理顧客訂單（接單、準備、完成）

## 📡 主要 API 端點

### 認證相關
- `POST /api/register` - 註冊新用戶
- `POST /api/login` - 用戶登入（需驗證碼）
- `GET /api/captcha` - 取得驗證碼
- `GET /api/profile` - 取得用戶資料

### OAuth 登入（可選）
- `GET /api/login/line/init` - LINE 登入
- `GET /api/login/google/init` - Google 登入

### 商家相關
- `GET /api/merchants` - 獲取商家列表
- `GET /api/merchants/:id/menu` - 獲取商家菜單

### 訂單相關
- `GET /api/orders` - 獲取訂單列表
- `POST /api/orders` - 創建訂單
- `PUT /api/orders/:id/status` - 更新訂單狀態

## ⚠️ 安全注意事項

**生產環境部署前請務必：**
1. 更改 `JWT_SECRET_KEY` 為強隨機字串
2. 設定強密碼保護 MySQL 資料庫
3. 啟用 HTTPS
4. 實作速率限制（Rate Limiting）
5. 確保 `.env` 文件不被提交到版本控制

## 📖 進階文檔

- **OAuth 設定指南** - 查看 `backend/env.example` 中的註解
- **API 詳細文檔** - 參考 `RESTAURANT_SYSTEM_README.md`
- **開發指南** - 參考 `DEVELOPMENT_GUIDE.md`

## 📄 授權

MIT License

---

**快速開始提示**：
1. 執行 `backend/init_database.sql` 初始化資料庫
2. 設定 `backend/.env` 環境變數
3. 啟動後端：`python backend/app.py`
4. 啟動前端：`cd frontend && npm run dev`
5. 訪問 `http://localhost:5173` 開始使用

