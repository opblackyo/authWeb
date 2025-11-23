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

- ✅ 用戶註冊（無需驗證碼，僅支援帳號密碼註冊）
- ✅ 用戶登入（需要驗證碼）
- ✅ JWT 認證
- ✅ 個人資料頁面
- ✅ 路由守衛
- ✅ 響應式設計
- ✅ 前後端分離架構
- ✅ OAuth 登入（LINE、Google）- **自動註冊功能**
- ✅ 帳號鎖定機制（可選，需資料庫支援）

**OAuth 登入說明**：
- OAuth 登入按鈕僅在登入頁面顯示
- 首次使用 OAuth 登入會自動創建帳號，無需手動註冊
- 註冊頁面不提供 OAuth 選項，僅支援傳統帳號密碼註冊

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

-- 建立 users 資料表（基本版本）
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) NULL,
    password VARCHAR(255) NULL,
    display_name VARCHAR(100) NULL,
    line_id VARCHAR(100) NULL UNIQUE,
    google_id VARCHAR(100) NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 添加索引以提高查詢效能
CREATE INDEX IF NOT EXISTS idx_line_id ON users(line_id);
CREATE INDEX IF NOT EXISTS idx_google_id ON users(google_id);
CREATE INDEX IF NOT EXISTS idx_username ON users(username);
```

**可選：啟用帳號鎖定功能**

如果需要啟用登入失敗鎖定功能（5 次失敗後鎖定 30 分鐘），可以執行以下 SQL 添加額外欄位：

```sql
USE vue_auth;

-- 添加帳號鎖定相關欄位
-- 注意：如果欄位已存在會報錯，可以忽略錯誤或先檢查欄位是否存在

-- 方法 1：直接添加（如果欄位不存在）
ALTER TABLE users 
ADD COLUMN failed_attempts INT DEFAULT 0,
ADD COLUMN lockout_until DATETIME NULL;

-- 方法 2：使用條件判斷（適用於 MariaDB 10.2.7+）
-- ALTER TABLE users 
-- ADD COLUMN IF NOT EXISTS failed_attempts INT DEFAULT 0,
-- ADD COLUMN IF NOT EXISTS lockout_until DATETIME NULL;
```

> **注意**：
> - 如果資料庫中沒有 `failed_attempts` 和 `lockout_until` 欄位，應用程式仍可正常運行，只是不會啟用帳號鎖定功能。應用程式會自動檢測這些欄位是否存在。
> - MySQL 5.7 不支援 `IF NOT EXISTS`，如果欄位已存在會報錯，可以忽略該錯誤。
> - 建議使用 `backend/database_update.sql` 腳本，它會處理欄位檢查。

**或使用更新腳本**：

如果資料庫已經存在，可以使用 `backend/database_update.sql` 腳本來更新資料庫結構：

```sql
-- 在 MySQL 中執行
source backend/database_update.sql;
```

或在 phpMyAdmin 中直接執行該 SQL 文件。

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
# CAPTCHA_SECRET_KEY=captcha-secret-key-change-in-production
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=你的MySQL密碼（如果有的話）
# DB_NAME=vue_auth
# 
# OAuth 設定（可選，如果不需要 OAuth 登入可以跳過）：
# LINE_CLIENT_ID=your-line-client-id
# LINE_CLIENT_SECRET=your-line-client-secret
# GOOGLE_CLIENT_ID=your-google-client-id
# GOOGLE_CLIENT_SECRET=your-google-client-secret
# FRONTEND_URL=http://localhost:5173  # 前端 URL（用於 OAuth 回調重定向）
```

### OAuth 登入設定（可選）

如果您想使用 Google 或 LINE 登入功能，需要先申請 OAuth 憑證。如果不需要此功能，可以跳過此步驟，但 OAuth 登入按鈕會顯示錯誤。

#### Google OAuth 設定步驟

1. **前往 Google Cloud Console**
   - 訪問：https://console.cloud.google.com/
   - 登入您的 Google 帳號

2. **建立新專案或選擇現有專案**
   - 點擊頂部專案選擇器
   - 點擊「新增專案」或選擇現有專案

3. **啟用 Google+ API**
   - 在左側選單選擇「API 和服務」>「程式庫」
   - 搜尋「Google+ API」並啟用

4. **建立 OAuth 2.0 憑證**
   - 前往「API 和服務」>「憑證」
   - 點擊「建立憑證」>「OAuth 用戶端 ID」
   - 如果首次使用，需要先設定「OAuth 同意畫面」：
     - 選擇「外部」或「內部」（根據您的需求）
     - 填寫應用程式名稱、使用者支援電子郵件等必填資訊
     - 儲存並繼續

5. **設定 OAuth 用戶端**
   - 應用程式類型：選擇「網頁應用程式」
   - 名稱：輸入應用程式名稱（例如：Auth Web App）
   - 已授權的重新導向 URI：
     ```
     http://localhost:5000/api/callback/google
     http://localhost:5000/api/callback/link/google
     ```
   - 點擊「建立」

6. **複製憑證資訊**
   - 複製「用戶端 ID」和「用戶端密鑰」
   - 將它們填入 `.env` 檔案：
     ```
     GOOGLE_CLIENT_ID=你的用戶端ID
     GOOGLE_CLIENT_SECRET=你的用戶端密鑰
     ```

#### LINE OAuth 設定步驟

1. **前往 LINE Developers Console**
   - 訪問：https://developers.line.biz/console/
   - 使用您的 LINE 帳號登入

2. **建立新 Provider**
   - 如果還沒有 Provider，點擊「建立」建立新的 Provider
   - 填寫 Provider 名稱和描述

3. **建立新 Channel**
   - 在 Provider 下點擊「建立 Channel」
   - 選擇「LINE Login」
   - 填寫 Channel 資訊：
     - Channel 名稱
     - Channel 說明
     - 應用程式類型：選擇「Web app」
     - 電子郵件地址

4. **設定 Callback URL**
   - 在 Channel 設定頁面找到「Callback URL」
   - 添加以下 URL：
     ```
     http://localhost:5000/api/callback/line
     http://localhost:5000/api/callback/link/line
     ```
   - 儲存設定

5. **取得 Channel ID 和 Channel Secret**
   - 在 Channel 設定頁面可以找到：
     - **Channel ID**（這是數字，不是字符串）
     - **Channel Secret**
   - 將它們填入 `.env` 檔案：
     ```
     LINE_CLIENT_ID=你的Channel_ID（純數字）
     LINE_CLIENT_SECRET=你的Channel_Secret
     ```

   > **重要**：LINE_CLIENT_ID 必須是純數字，不要加引號或任何其他字符。

#### OAuth 登入自動註冊功能

**重要說明**：OAuth 登入（LINE 和 Google）具有自動註冊功能：

- 如果用戶首次使用 OAuth 登入，系統會**自動創建新帳號**
- 如果用戶已經存在（根據 LINE ID 或 Google ID），則直接登入
- **不需要**在註冊頁面使用 OAuth，只需在登入頁面點擊 OAuth 按鈕即可
- 註冊頁面已移除 OAuth 按鈕，只保留傳統的帳號密碼註冊方式

#### OAuth 登入流程

1. 用戶在登入頁面點擊「LINE 登入」或「Google 登入」按鈕
2. 系統跳轉到對應的 OAuth 授權頁面
3. 用戶授權後，OAuth 提供者會重定向回後端回調 URL
4. 後端處理登入/註冊，生成 JWT token
5. **自動重定向到前端 OAuth 回調頁面**（`/oauth/callback`）
6. 前端自動保存 token 並跳轉到首頁
7. **無需手動複製 token**，整個流程自動完成

#### 驗證 OAuth 設定

1. **設定前端 URL**（可選）：
   
   在 `.env` 檔案中添加：
   ```
   FRONTEND_URL=http://localhost:5173
   ```
   
   如果不設定，預設為 `http://localhost:5173`

2. **重新啟動後端伺服器**：
   ```bash
   python app.py
   ```

3. **測試 OAuth 登入**：
   - 在前端登入頁面點擊 OAuth 按鈕
   - 應該會跳轉到對應的授權頁面
   - 授權後會自動重定向回前端並完成登入
   - 首次使用會自動註冊並登入

#### OAuth 登入常見問題

**問題 1：`authStore.setAuth is not a function`**
- **原因**：前端 store 中 `setAuth` 方法未正確導出
- **解決**：已修復，確保 `setAuth` 和 `clearAuth` 方法在 store 的 return 中導出

**問題 2：`'utf-8' codec can't decode bytes` 或 `無法解析 LINE id_token`**
- **原因**：
  - URL 參數中的特殊字符（特別是 JWT token）沒有正確編碼
  - LINE API 返回的 id_token 中的 base64 編碼數據可能包含非 UTF-8 字符
  - base64 解碼後的 payload 可能無法用 UTF-8 正確解碼
- **解決**：
  - 後端現在使用 `urllib.parse.quote` 正確編碼所有 URL 參數（包括使用 `safe=''` 確保所有字符都被編碼）
  - **改進了 LINE id_token 解析**：
    - 如果 id_token 解析失敗，自動切換到使用 access_token 獲取用戶資訊
    - 使用 `errors='replace'` 處理 UTF-8 解碼錯誤，避免崩潰
    - 添加了完整的錯誤處理，不會因為 id_token 解析失敗而中斷登入流程
  - 前端改進了錯誤訊息的解碼處理，使用 try-catch 避免解碼失敗
  - 錯誤訊息在編碼前會檢查是否為有效的 UTF-8 字符串

**問題 3：OAuth 登入後沒有自動跳轉**
- **檢查**：確認 `.env` 中的 `FRONTEND_URL` 設定正確
- **檢查**：確認前端路由中已添加 `/oauth/callback` 路由
- **檢查**：查看瀏覽器控制台是否有 JavaScript 錯誤

**問題 4：OAuth 登入後顯示錯誤頁面**
- **檢查**：查看錯誤訊息內容
- **檢查**：確認 OAuth 憑證（CLIENT_ID 和 CLIENT_SECRET）設定正確
- **檢查**：確認 Callback URL 在 OAuth 提供者設定中正確配置

#### 如果不需要 OAuth 功能

如果您不需要 OAuth 登入功能，可以：

1. **隱藏 OAuth 按鈕**（需要修改前端代碼）
2. **保留預設值**：不設定 OAuth 憑證，點擊按鈕時會顯示錯誤訊息，但不影響其他功能
3. **設定空值**：在 `.env` 中設定為空字串：
   ```
   LINE_CLIENT_ID=
   LINE_CLIENT_SECRET=
   GOOGLE_CLIENT_ID=
   GOOGLE_CLIENT_SECRET=
   ```

#### 常見錯誤

- **Google OAuth 錯誤 401: invalid_client**
  - 原因：`GOOGLE_CLIENT_ID` 或 `GOOGLE_CLIENT_SECRET` 未正確設定
  - 解決：檢查 `.env` 檔案中的值是否正確，確保沒有多餘的空格或引號

- **LINE OAuth 錯誤 400: Bad Request - clientId 類型錯誤**
  - 原因：`LINE_CLIENT_ID` 應該是純數字，但設定為字符串（如 "your-line-client-id"）
  - 解決：將 `LINE_CLIENT_ID` 設定為從 LINE Developers Console 取得的數字 ID

- **Redirect URI mismatch**
  - 原因：在 OAuth 提供者設定的 Callback URL 與程式碼中的不一致
  - 解決：確保兩邊的 URL 完全一致（包括 http/https、端口號等）
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
  "password": "password123",
  "confirm_password": "password123"
}
```

**注意**：
- 使用者名稱至少需要 4 個字元
- 密碼至少需要 6 個字元
- 不需要驗證碼（註冊功能已移除驗證碼要求）

### POST /api/login
用戶登入

請求體：
```json
{
  "username": "testuser",
  "password": "password123",
  "captcha_answer": "ABCD",
  "captcha_token": "captcha_token_here"
}
```

**注意**：
- 登入需要驗證碼（先呼叫 GET /api/captcha 取得驗證碼圖片和 token）
- 如果資料庫有 `failed_attempts` 和 `lockout_until` 欄位，5 次登入失敗後會鎖定帳號 30 分鐘

回應：
```json
{
  "message": "登入成功",
  "token": "jwt_token_here",
  "user": "testuser",
  "expires_in": 1800
}
```

### GET /api/captcha
取得驗證碼圖片和 token（用於登入）

回應：
```json
{
  "captcha_token": "token_here",
  "image": "data:image/png;base64,..."
}
```

### GET /api/profile
取得用戶個人資料（需要 JWT token）

Headers:
```
Authorization: Bearer <token>
```

回應：
```json
{
  "message": "test success",
  "user_id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "display_name": null,
  "is_line_linked": false,
  "is_google_linked": false
}
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

## Git 版本控制

### 初始化 Git 倉庫

如果是新專案，初始化 Git：

```bash
# 初始化 Git 倉庫
git init

# 添加所有文件（.gitignore 會自動排除敏感文件）
git add .

# 提交初始版本
git commit -m "Initial commit"
```

### 避免敏感文件外洩

**重要**：為了保護敏感資訊，請確保以下文件**永遠不要**提交到 Git：

1. **環境變數文件**：
   - `.env` - 包含資料庫密碼、JWT 密鑰、OAuth 憑證等
   - `.env.local` - 本地環境變數
   - 任何包含實際密鑰的配置文件

2. **資料庫文件**：
   - `*.db` - SQLite 資料庫文件
   - `auth.db` - 專案資料庫文件

3. **虛擬環境**：
   - `venv/` - Python 虛擬環境
   - `node_modules/` - Node.js 依賴包

#### 檢查 .gitignore 設定

專案已包含 `.gitignore` 文件，會自動排除敏感文件。請確認：

```bash
# 檢查 .gitignore 是否正確設定
cat .gitignore
cat backend/.gitignore
cat frontend/.gitignore
```

#### 如果已經提交了敏感文件

**緊急處理步驟**：

1. **立即從 Git 歷史中移除敏感文件**：
   ```bash
   # 從 Git 中移除文件但保留本地文件
   git rm --cached backend/.env
   git rm --cached backend/auth.db
   
   # 提交移除操作
   git commit -m "Remove sensitive files from Git"
   ```

2. **清理 Git 歷史**（如果敏感文件已經被推送）：
   ```bash
   # 使用 git filter-branch 或 BFG Repo-Cleaner 清理歷史
   # 注意：這會重寫 Git 歷史，需要強制推送
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch backend/.env backend/auth.db" \
     --prune-empty --tag-name-filter cat -- --all
   ```

3. **立即更改所有已洩露的密鑰**：
   - 更改資料庫密碼
   - 重新生成 JWT_SECRET_KEY
   - 重新生成 OAuth 憑證（如果已洩露）

4. **強制推送**（僅在清理歷史後）：
   ```bash
   # 警告：這會覆蓋遠程倉庫歷史
   git push origin --force --all
   ```

#### 提交前檢查

在每次提交前，檢查是否包含敏感文件：

```bash
# 檢查即將提交的文件
git status

# 檢查是否有 .env 文件被追蹤
git ls-files | grep -E "\.env$|auth\.db$"

# 如果發現敏感文件，從 Git 中移除
git rm --cached <文件路徑>
```

#### 使用 .env.example 作為模板

專案包含 `backend/env.example` 文件，這是環境變數的模板：

```bash
# 複製模板創建實際的 .env 文件（不要提交 .env）
cp backend/env.example backend/.env

# 編輯 .env 文件，填入實際的配置值
# .env 文件會被 .gitignore 自動排除
```

#### Git 最佳實踐

1. **提交前檢查**：
   ```bash
   git status
   git diff
   ```

2. **使用有意義的提交訊息**：
   ```bash
   git commit -m "feat: 添加 OAuth 登入功能"
   git commit -m "fix: 修復驗證碼生成錯誤"
   ```

3. **定期提交**：
   ```bash
   git add .
   git commit -m "描述你的更改"
   git push origin main
   ```

4. **使用分支開發**：
   ```bash
   # 創建功能分支
   git checkout -b feature/new-feature
   
   # 開發完成後合併
   git checkout main
   git merge feature/new-feature
   ```

#### 檢查敏感資訊的工具

可以使用工具檢查是否意外提交了敏感資訊：

```bash
# 使用 git-secrets（需要先安裝）
git secrets --scan

# 或使用 truffleHog 掃描 Git 歷史
# pip install truffleHog
trufflehog --regex --entropy=False .
```

## 授權

MIT License

