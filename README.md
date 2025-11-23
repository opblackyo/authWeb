# 餐廳訂餐系統 - 身分分流平台

這是一個使用 Python Flask + MySQL (XAMPP) 作為後端，Vue 3 作為前端的**餐廳訂餐系統**，支援**顧客**和**商家**兩種角色的身分分流。

## 🎯 系統特色

- **身分分流系統**：註冊時選擇角色（顧客/商家），登入後自動導向對應介面
- **顧客介面**：瀏覽餐廳、查看菜單、下訂單、訂單追蹤
- **商家介面**：接單看板、訂單管理、菜單管理、營業統計
- **共用元件庫**：統一的 UI 元件（按鈕、輸入框、卡片、下拉選單）
- **完整認證系統**：JWT + OAuth（LINE、Google）+ 帳號鎖定機制

## 📚 文件導覽

- **[RESTAURANT_SYSTEM_README.md](./RESTAURANT_SYSTEM_README.md)** - 餐廳系統完整說明
- **[DEVELOPMENT_GUIDE.md](./DEVELOPMENT_GUIDE.md)** - 開發指南和元件使用說明
- **本文件** - 基礎安裝和設定指南

## 專案結構

```
authWeb/
├── backend/
│   ├── app.py                    # Flask 主應用（包含角色系統 API）
│   ├── migrations/               # 資料庫遷移腳本
│   │   └── add_user_role.sql    # 角色系統遷移
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api/                  # API 服務層
│   │   │   └── auth.js          # 認證 API（支援角色）
│   │   ├── components/
│   │   │   ├── common/          # 共用元件庫 ⭐
│   │   │   │   ├── BaseButton.vue
│   │   │   │   ├── BaseInput.vue
│   │   │   │   ├── BaseCard.vue
│   │   │   │   └── BaseSelect.vue
│   │   │   ├── Header.vue       # 頂部導航欄
│   │   │   └── Sidebar.vue      # 側邊欄
│   │   ├── layouts/
│   │   │   └── DashboardLayout.vue  # Dashboard 佈局
│   │   ├── stores/
│   │   │   └── auth.js          # 認證狀態管理（包含角色）
│   │   ├── views/               # 頁面組件
│   │   ├── router/
│   │   │   └── index.js         # 路由配置（角色守衛）
│   │   └── main.js
│   └── package.json
├── README.md                     # 本文件
├── RESTAURANT_SYSTEM_README.md   # 餐廳系統說明 ⭐
└── DEVELOPMENT_GUIDE.md          # 開發指南 ⭐
```

## 功能特色

### 🔐 認證系統
- ✅ 用戶註冊（支援角色選擇：顧客/商家）
- ✅ 用戶登入（需要驗證碼）
- ✅ JWT 認證
- ✅ OAuth 登入（LINE、Google）- **自動註冊功能**
- ✅ 帳號鎖定機制（防暴力破解）
- ✅ 路由守衛和角色權限控制

### 👥 顧客功能
- ✅ 瀏覽餐廳列表
- ✅ 查看餐廳菜單
- ✅ 購物車功能
- ✅ 下訂單
- ✅ 訂單歷史和追蹤
- ✅ 個人資料管理

### 🏪 商家功能
- ✅ 接單看板（Dashboard）
- ✅ 訂單管理（接單、準備中、完成）
- ✅ 菜單管理（新增、編輯、刪除）
- ✅ 商家資料管理
- ✅ 營業統計報表

### 🎨 共用元件庫
- ✅ BaseButton - 統一按鈕組件（7 種樣式、3 種尺寸）
- ✅ BaseInput - 統一輸入框組件（支援驗證、圖標、密碼切換）
- ✅ BaseCard - 統一卡片組件（4 種變體）
- ✅ BaseSelect - 統一下拉選單組件

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
```

3. **執行資料庫遷移腳本**（包含角色系統）：

```bash
# 在 MySQL 中執行遷移腳本
mysql -u root -p vue_auth < backend/migrations/add_user_role.sql
```

或在 phpMyAdmin 中直接執行 `backend/migrations/add_user_role.sql` 文件。

**遷移腳本會創建以下資料表：**
- `users` - 用戶表（包含 role 欄位）
- `merchants` - 商家表
- `menu_items` - 菜單項目表
- `orders` - 訂單表
- `order_items` - 訂單項目表

4. 進入後端目錄：
```bash
cd backend
```

5. 建立虛擬環境（建議）：
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

6. 安裝依賴：
```bash
pip install -r requirements.txt
```

7. 設定環境變數：
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

8. 執行後端：
```bash
python app.py
```

後端將在 `http://localhost:5000` 運行

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

## 快速開始

### 測試顧客流程

1. 訪問 `http://localhost:5173/register`
2. 選擇角色：**顧客**
3. 填寫用戶名和密碼，完成註冊
4. 登入後自動導向餐廳首頁
5. 瀏覽餐廳、查看菜單、下訂單

### 測試商家流程

1. 訪問 `http://localhost:5173/register`
2. 選擇角色：**商家**
3. 填寫用戶名、密碼和商家名稱，完成註冊
4. 登入後自動導向接單看板
5. 查看訂單、管理菜單、處理訂單

## API 端點

### 認證 API

#### POST /api/register
註冊新用戶（支援角色選擇）

請求體：
```json
{
  "username": "testuser",
  "password": "password123",
  "confirm_password": "password123",
  "role": "customer",
  "display_name": "測試用戶",
  "email": "test@example.com",
  "phone": "0912345678",
  "business_name": "我的餐廳"
}
```

**注意**：
- `role`: 必填，可選值為 `customer`（顧客）或 `merchant`（商家）
- `business_name`: 僅當 `role` 為 `merchant` 時需要
- 使用者名稱至少需要 4 個字元
- 密碼至少需要 6 個字元

#### POST /api/login
用戶登入（返回角色資訊）

請求體：
```json
{
  "username": "testuser",
  "password": "password123",
  "captcha_answer": "ABCD",
  "captcha_token": "captcha_token_here"
}
```

回應：
```json
{
  "message": "登入成功",
  "token": "jwt_token_here",
  "user": "testuser",
  "role": "customer",
  "display_name": "測試用戶",
  "email": "test@example.com",
  "phone": "0912345678",
  "merchant": {
    "id": 1,
    "business_name": "我的餐廳",
    "business_type": "中式料理",
    "rating": 4.5
  },
  "expires_in": 1800
}
```

**注意**：
- 登入需要驗證碼（先呼叫 GET /api/captcha 取得驗證碼圖片和 token）
- 如果是商家角色，回應中會包含 `merchant` 物件
- 5 次登入失敗後會鎖定帳號 30 分鐘

#### GET /api/captcha
取得驗證碼圖片和 token（用於登入）

回應：
```json
{
  "captcha_token": "token_here",
  "image": "data:image/png;base64,..."
}
```

#### GET /api/profile
取得用戶個人資料（包含角色和商家資訊）

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
  "role": "merchant",
  "email": "test@example.com",
  "display_name": "測試用戶",
  "phone": "0912345678",
  "is_line_linked": false,
  "is_google_linked": false,
  "merchant": {
    "id": 1,
    "business_name": "我的餐廳",
    "business_type": "中式料理",
    "address": "台北市信義區",
    "description": "提供美味的中式料理",
    "is_verified": true,
    "rating": 4.5
  }
}
```

### 商家 API

#### GET /api/merchants
獲取商家列表

#### GET /api/merchants/:id
獲取商家詳情

#### GET /api/merchants/:id/menu
獲取商家菜單

### 訂單 API

#### GET /api/orders
獲取訂單列表（根據角色返回不同數據）
- 顧客：返回自己的訂單
- 商家：返回自己店鋪的訂單

#### POST /api/orders
創建訂單

#### PUT /api/orders/:id/status
更新訂單狀態（僅商家）

**詳細 API 文件請參考 [RESTAURANT_SYSTEM_README.md](./RESTAURANT_SYSTEM_README.md)**

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

