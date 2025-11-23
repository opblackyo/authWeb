# 開發指南 - 餐廳訂餐系統

## 專案結構

```
authWeb/
├── backend/
│   ├── app.py                    # Flask 主應用
│   ├── migrations/               # 資料庫遷移腳本
│   │   └── add_user_role.sql    # 角色系統遷移
│   ├── requirements.txt          # Python 依賴
│   └── .env                      # 環境變數（不提交）
│
├── frontend/
│   ├── src/
│   │   ├── api/                  # API 服務層
│   │   │   └── auth.js          # 認證 API
│   │   ├── components/
│   │   │   ├── common/          # 共用元件庫
│   │   │   │   ├── BaseButton.vue
│   │   │   │   ├── BaseInput.vue
│   │   │   │   ├── BaseCard.vue
│   │   │   │   └── BaseSelect.vue
│   │   │   ├── Header.vue       # 頂部導航欄
│   │   │   └── Sidebar.vue      # 側邊欄
│   │   ├── layouts/
│   │   │   └── DashboardLayout.vue  # Dashboard 佈局
│   │   ├── stores/
│   │   │   └── auth.js          # 認證狀態管理
│   │   ├── views/
│   │   │   ├── LoginView.vue    # 登入頁面
│   │   │   ├── RegisterView.vue # 註冊頁面
│   │   │   ├── DashboardView.vue # 儀表板
│   │   │   ├── ProfileView.vue  # 個人資料
│   │   │   └── SettingsView.vue # 設定頁面
│   │   ├── router/
│   │   │   └── index.js         # 路由配置
│   │   └── main.js              # 應用入口
│   └── package.json
│
├── README.md                     # 原始專案說明
├── RESTAURANT_SYSTEM_README.md   # 餐廳系統說明
└── DEVELOPMENT_GUIDE.md          # 本文件
```

## 共用元件庫使用指南

### BaseButton 組件

統一的按鈕組件，支援多種樣式和狀態。

**Props：**
- `variant`: 按鈕樣式（primary, secondary, success, danger, warning, outline, ghost）
- `size`: 按鈕大小（small, medium, large）
- `icon`: 圖標（emoji 或文字）
- `loading`: 載入狀態
- `disabled`: 禁用狀態

**使用範例：**
```vue
<template>
  <BaseButton variant="primary" size="medium" @click="handleClick">
    提交訂單
  </BaseButton>
  
  <BaseButton variant="success" icon="✓" :loading="isLoading">
    確認
  </BaseButton>
  
  <BaseButton variant="outline" size="small">
    取消
  </BaseButton>
</template>

<script setup>
import BaseButton from '@/components/common/BaseButton.vue'
</script>
```

### BaseInput 組件

統一的輸入框組件，支援驗證和圖標。

**Props：**
- `modelValue`: v-model 綁定值
- `type`: 輸入類型（text, password, email, number 等）
- `label`: 標籤文字
- `placeholder`: 佔位符
- `icon`: 圖標（emoji 或文字）
- `error`: 錯誤訊息
- `hint`: 提示訊息
- `required`: 必填標記
- `disabled`: 禁用狀態

**使用範例：**
```vue
<template>
  <BaseInput
    v-model="username"
    label="用戶名"
    placeholder="請輸入用戶名"
    icon="👤"
    :error="usernameError"
    required
  />
  
  <BaseInput
    v-model="password"
    type="password"
    label="密碼"
    icon="🔒"
    hint="密碼至少 6 個字元"
  />
</template>

<script setup>
import { ref } from 'vue'
import BaseInput from '@/components/common/BaseInput.vue'

const username = ref('')
const password = ref('')
const usernameError = ref('')
</script>
```

### BaseCard 組件

統一的卡片組件，支援多種變體。

**Props：**
- `title`: 卡片標題
- `variant`: 卡片樣式（default, bordered, elevated, flat）
- `hoverable`: 懸停效果
- `clickable`: 可點擊
- `noPadding`: 無內邊距

**Slots：**
- `header`: 自訂頭部
- `default`: 主要內容
- `footer`: 底部內容

**使用範例：**
```vue
<template>
  <BaseCard title="訂單詳情" variant="elevated">
    <p>訂單編號：#12345</p>
    <p>總金額：$250</p>
    
    <template #footer>
      <BaseButton variant="primary">查看詳情</BaseButton>
    </template>
  </BaseCard>
</template>

<script setup>
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
</script>
```

### BaseSelect 組件

統一的下拉選單組件。

**Props：**
- `modelValue`: v-model 綁定值
- `label`: 標籤文字
- `placeholder`: 佔位符
- `options`: 選項陣列 `[{ value, label }]`
- `error`: 錯誤訊息
- `required`: 必填標記

**使用範例：**
```vue
<template>
  <BaseSelect
    v-model="selectedRole"
    label="選擇角色"
    :options="roleOptions"
    required
  />
</template>

<script setup>
import { ref } from 'vue'
import BaseSelect from '@/components/common/BaseSelect.vue'

const selectedRole = ref('')
const roleOptions = [
  { value: 'customer', label: '顧客' },
  { value: 'merchant', label: '商家' }
]
</script>
```

## 狀態管理（Pinia Store）

### Auth Store

認證狀態管理，包含用戶資訊和角色。

**State：**
- `token`: JWT Token
- `user`: 用戶資訊（包含 role, display_name, email 等）

**Getters：**
- `isAuthenticated`: 是否已登入
- `userRole`: 用戶角色（customer/merchant）
- `isCustomer`: 是否為顧客
- `isMerchant`: 是否為商家

**Actions：**
- `login(username, password, captchaAnswer, captchaToken)`: 登入
- `register(username, password, confirmPassword, role, additionalData)`: 註冊
- `logout()`: 登出
- `fetchProfile()`: 獲取個人資料
- `setAuth(token, userData)`: 設定認證資訊
- `clearAuth()`: 清除認證資訊

**使用範例：**
```vue
<script setup>
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// 檢查用戶角色
if (authStore.isCustomer) {
  // 顧客邏輯
} else if (authStore.isMerchant) {
  // 商家邏輯
}

// 登入
const handleLogin = async () => {
  const result = await authStore.login(username, password, captcha, token)
  if (result.success) {
    // 根據角色導向不同頁面
    if (result.role === 'customer') {
      router.push('/restaurant')
    } else {
      router.push('/merchant/dashboard')
    }
  }
}
</script>
```

## 路由守衛

### 角色驗證

路由守衛會根據用戶角色自動導向對應頁面。

**Meta 欄位：**
- `requiresAuth`: 需要登入
- `requiresRole`: 需要特定角色（customer/merchant）
- `requiresGuest`: 需要未登入

**範例：**
```javascript
{
  path: '/restaurant',
  component: RestaurantLayout,
  meta: { requiresAuth: true, requiresRole: 'customer' },
  children: [...]
}

{
  path: '/merchant/dashboard',
  component: MerchantLayout,
  meta: { requiresAuth: true, requiresRole: 'merchant' },
  children: [...]
}
```

## API 開發規範

### 請求格式

所有 API 請求使用 JSON 格式，並在 Header 中包含 JWT Token（需要認證的端點）。

```javascript
// 範例：創建訂單
const createOrder = async (orderData) => {
  return api.post('/api/orders', {
    merchant_id: orderData.merchantId,
    items: orderData.items,
    note: orderData.note
  })
}
```

### 回應格式

統一的回應格式：

```json
{
  "message": "操作成功",
  "data": { ... },
  "error": null
}
```

錯誤回應：

```json
{
  "message": "錯誤訊息",
  "error": "ERROR_CODE"
}
```

## 開發流程

### 1. 創建新功能

1. **規劃資料結構**：確定需要的資料表和欄位
2. **設計 API**：定義 API 端點和請求/回應格式
3. **實作後端**：在 `backend/app.py` 中添加 API 端點
4. **實作前端**：創建 Vue 組件和頁面
5. **測試**：測試功能是否正常運作

### 2. 使用共用元件

優先使用共用元件庫中的元件，保持 UI 一致性：

```vue
<!-- ✅ 推薦：使用共用元件 -->
<BaseButton variant="primary" @click="submit">提交</BaseButton>

<!-- ❌ 不推薦：自己寫按鈕 -->
<button class="my-custom-button" @click="submit">提交</button>
```

### 3. 狀態管理

使用 Pinia Store 管理全局狀態，避免 prop drilling：

```vue
<!-- ✅ 推薦：使用 Store -->
<script setup>
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
const username = authStore.user?.username
</script>

<!-- ❌ 不推薦：層層傳遞 props -->
<Parent :user="user">
  <Child :user="user">
    <GrandChild :user="user" />
  </Child>
</Parent>
```

### 4. 錯誤處理

統一的錯誤處理方式：

```javascript
try {
  const result = await authStore.login(username, password, captcha, token)
  if (result.success) {
    // 成功處理
  } else {
    // 顯示錯誤訊息
    errorMessage.value = result.error
  }
} catch (error) {
  // 處理異常
  console.error('登入失敗:', error)
}
```

## 測試指南

### 手動測試流程

1. **顧客流程測試**
   - 註冊顧客帳號
   - 登入並驗證導向餐廳首頁
   - 瀏覽餐廳和菜單
   - 下訂單
   - 查看訂單狀態

2. **商家流程測試**
   - 註冊商家帳號
   - 登入並驗證導向接單看板
   - 查看訂單列表
   - 更新訂單狀態
   - 管理菜單

3. **角色權限測試**
   - 驗證顧客無法訪問商家頁面
   - 驗證商家無法訪問顧客頁面
   - 驗證未登入用戶被導向登入頁面

## 部署注意事項

### 生產環境檢查清單

- [ ] 更改 JWT_SECRET_KEY 為強隨機字串
- [ ] 設定正確的 CORS 來源
- [ ] 啟用 HTTPS
- [ ] 設定資料庫備份
- [ ] 實作速率限制
- [ ] 添加日誌記錄
- [ ] 設定錯誤監控
- [ ] 優化圖片上傳和存儲
- [ ] 實作快取機制
- [ ] 壓縮前端資源

## 常見問題

### Q: 如何添加新的用戶角色？

A: 需要修改以下位置：
1. 資料庫：修改 `users.role` 欄位的 ENUM 值
2. 後端：更新 `app.py` 中的角色驗證邏輯
3. 前端：更新 `auth.js` store 和路由守衛

### Q: 如何自訂共用元件樣式？

A: 共用元件支援通過 props 自訂樣式，如需更深度自訂，可以：
1. 使用 CSS 變數覆蓋
2. 創建新的變體（variant）
3. 繼承基礎元件並擴展

### Q: 如何處理圖片上傳？

A: 建議使用以下方案：
1. 本地開發：存儲在 `backend/uploads/` 目錄
2. 生產環境：使用雲端存儲服務（如 AWS S3、阿里雲 OSS）

## 授權

MIT License

