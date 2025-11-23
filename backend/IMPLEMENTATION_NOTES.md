# API 實現說明

## 已實現的功能

根據 API 規範，已實現以下功能：

### 1. 驗證碼 API
- ✅ GET /api/captcha - 取得驗證碼圖片和 token

### 2. 身份驗證 API
- ✅ POST /api/register - 註冊新帳號（支持驗證碼、確認密碼）
- ✅ POST /api/login - 帳號密碼登入（支持驗證碼、帳號鎖定機制）

### 3. 帳號管理 API（需驗證）
- ✅ GET /api/profile - 取得當前登入使用者的個人資料
- ✅ POST /api/user/username - 變更使用者名稱（返回新 token）
- ✅ POST /api/user/password - 變更帳號密碼

### 4. OAuth 登入/註冊 API
- ✅ GET /api/login/line/init - LINE 登入/註冊初始化
- ✅ GET /api/login/google/init - Google 登入/註冊初始化
- ✅ GET /api/callback/line - LINE OAuth 回調
- ✅ GET /api/callback/google - Google OAuth 回調

### 5. OAuth 綁定 API（需驗證）
- ✅ GET /api/link/line/init - LINE 帳號綁定初始化
- ✅ GET /api/link/google/init - Google 帳號綁定初始化
- ✅ GET /api/callback/link/line - LINE 綁定回調
- ✅ GET /api/callback/link/google - Google 綁定回調

## 安裝步驟

### 1. 更新後端依賴

```bash
cd backend
pip install -r requirements.txt
```

新增的套件：
- `captcha==0.4.0` - 驗證碼生成
- `Pillow==10.0.0` - 圖像處理
- `requests==2.31.0` - HTTP 請求（OAuth 用）

### 2. 更新資料庫結構

執行 `database_update.sql` 腳本更新資料庫：

```sql
-- 在 MySQL 中執行
source database_update.sql;
```

或直接在 phpMyAdmin 中執行該 SQL 文件。

### 3. 配置環境變數

複製 `env.example` 為 `.env` 並填入配置：

```bash
cp env.example .env
```

需要配置的項目：
- `JWT_SECRET_KEY` - JWT 密鑰
- `CAPTCHA_SECRET_KEY` - 驗證碼密鑰
- `LINE_CLIENT_ID` / `LINE_CLIENT_SECRET` - LINE OAuth（可選）
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` - Google OAuth（可選）

### 4. 啟動後端

```bash
python app.py
```

後端將運行在 `http://localhost:5000`

### 5. 啟動前端

```bash
cd frontend
npm install
npm run dev
```

前端將運行在 `http://localhost:5173`

## 資料庫變更說明

### 新增欄位
- `display_name` - 顯示名稱（OAuth 用戶）
- `line_id` - LINE 帳號 ID（唯一）
- `google_id` - Google 帳號 ID（唯一）
- `failed_attempts` - 登入失敗次數
- `lockout_until` - 鎖定到期時間

### 修改欄位
- `email` - 改為可選（OAuth 用戶可能沒有）
- `password` - 改為可選（OAuth 用戶可能沒有）

## API 使用說明

### 驗證碼流程
1. 前端調用 `GET /api/captcha` 獲取驗證碼圖片和 token
2. 用戶輸入驗證碼
3. 在註冊/登入時一併提交 `captcha_answer` 和 `captcha_token`

### 帳號鎖定機制
- 登入失敗 5 次後，帳號將被鎖定 30 分鐘
- 鎖定期間無法登入，會返回 403 錯誤

### OAuth 登入流程
1. 前端調用 `GET /api/login/{provider}/init` 獲取授權 URL
2. 將用戶導向授權 URL
3. 用戶授權後，OAuth 提供商會重定向到 callback
4. Callback 頁面會顯示 JSON 格式的 token，用戶需要手動複製

### OAuth 綁定流程
1. 用戶必須先登入（需要 JWT token）
2. 前端調用 `GET /api/link/{provider}/init` 獲取授權 URL
3. 將用戶導向授權 URL
4. 用戶授權後，OAuth 提供商會重定向到綁定 callback
5. 綁定成功後，callback 頁面會顯示成功訊息

## 注意事項

1. **驗證碼存儲**：目前使用內存存儲驗證碼，生產環境應使用 Redis
2. **OAuth 配置**：需要在 LINE/Google 開發者平台配置 redirect URI
3. **Token 過期時間**：JWT token 有效期為 30 分鐘（1800 秒）
4. **密碼要求**：至少 6 個字元
5. **使用者名稱要求**：至少 4 個字元

## 錯誤處理

所有 API 錯誤都會返回適當的 HTTP 狀態碼和錯誤訊息：
- `400` - 請求參數錯誤
- `401` - 未授權（登入失敗、token 無效）
- `403` - 帳號被鎖定
- `409` - 資源衝突（用戶名已存在、OAuth 帳號已被綁定）
- `500` - 伺服器錯誤


