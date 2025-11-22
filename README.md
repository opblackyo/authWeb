# 前後端分離登入系統

這是一個使用 Python Flask + MySQL (XAMPP) 作為後端，Vue 3 作為前端的登入系統專案。

## 專案結構

```
authWeb/
├── backend/          # Python Flask 後端
│   ├── app.py       # 主應用程式
│   ├── requirements.txt
│   └── .env.example
├── frontend/        # Vue 3 前端
│   ├── src/
│   │   ├── api/     # API 服務
│   │   ├── stores/  # Pinia 狀態管理
│   │   ├── views/   # 頁面組件
│   │   ├── router/  # 路由配置
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 功能特色

- ✅ 用戶註冊
- ✅ 用戶登入
- ✅ JWT 認證
- ✅ 個人資料頁面
- ✅ 路由守衛
- ✅ 響應式設計
- ✅ 前後端分離架構

## 技術棧

### 後端
- Python 3.x
- Flask
- Flask-JWT-Extended
- MySQL (XAMPP)
- PyMySQL
- Flask-CORS

### 前端
- Vue 3 (Composition API)
- Vue Router
- Pinia
- Axios
- Vite

## 安裝與執行

### 後端設定

1. **啟動 XAMPP 並確保 MySQL 服務正在運行**

2. **建立資料庫和資料表**：
   
   開啟 phpMyAdmin (http://localhost/phpmyadmin) 或使用 MySQL 命令列，執行以下 SQL 指令：

```sql
-- 建立資料庫
CREATE DATABASE IF NOT EXISTS vue_auth CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用資料庫
USE vue_auth;

-- 建立 users 資料表
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

3. 進入後端目錄：
```bash
cd backend
```

4. 建立虛擬環境（建議）：
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

5. 安裝依賴：
```bash
pip install -r requirements.txt
```

6. 設定環境變數：
```bash
# 複製 env.example 為 .env
# Windows
copy env.example .env
# Linux/Mac
cp env.example .env

# 編輯 .env 檔案，設定以下變數：
# JWT_SECRET_KEY=your-secret-key
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=你的MySQL密碼（如果有的話）
# DB_NAME=vue_auth
```

7. 執行後端：
```bash
python app.py
```

後端將在 `http://localhost:5000` 運行

### 前端設定

1. 進入前端目錄：
```bash
cd frontend
```

2. 安裝依賴：
```bash
npm install
```

3. 執行開發伺服器：
```bash
npm run dev
```

前端將在 `http://localhost:5173` 運行

## API 端點

### POST /api/register
註冊新用戶

請求體：
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

### POST /api/login
用戶登入

請求體：
```json
{
  "username": "testuser",
  "password": "password123"
}
```

回應：
```json
{
  "access_token": "jwt_token_here",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

### GET /api/profile
取得用戶個人資料（需要 JWT token）

Headers:
```
Authorization: Bearer <token>
```

## 安全注意事項

⚠️ **生產環境注意事項：**

1. 更改 `JWT_SECRET_KEY` 為強隨機字串
2. 使用環境變數管理敏感資訊
3. 啟用 HTTPS
4. 實作速率限制（Rate Limiting）
5. 設定強密碼保護 MySQL 資料庫
6. 實作密碼強度驗證
7. 添加 CSRF 保護
8. 實作日誌記錄和監控

## 開發建議

- 使用 VS Code 搭配 Volar 擴充套件進行 Vue 開發
- 使用 Vue Devtools 進行除錯
- 遵循 Vue 3 Composition API 最佳實踐
- 保持組件小而專注
- 使用 TypeScript 提升類型安全（可選）

## 授權

MIT License

