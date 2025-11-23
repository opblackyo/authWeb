-- 添加用戶角色欄位
-- 執行此腳本以更新資料庫結構

-- 添加 role 欄位到 users 表
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS role ENUM('customer', 'merchant') NOT NULL DEFAULT 'customer' AFTER username;

-- 添加 display_name 欄位（顯示名稱）
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS display_name VARCHAR(100) AFTER role;

-- 添加 phone 欄位（電話號碼）
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS phone VARCHAR(20) AFTER display_name;

-- 添加 email 欄位（電子郵件）
ALTER TABLE users
ADD COLUMN IF NOT EXISTS email VARCHAR(255) AFTER phone;

-- 添加 failed_attempts 欄位（登入失敗次數）
ALTER TABLE users
ADD COLUMN IF NOT EXISTS failed_attempts INT DEFAULT 0 AFTER email;

-- 添加 lockout_until 欄位（帳號鎖定時間）
ALTER TABLE users
ADD COLUMN IF NOT EXISTS lockout_until DATETIME NULL AFTER failed_attempts;

-- 添加索引以提高查詢效率
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- 創建商家資料表（用於存儲商家特定資訊）
CREATE TABLE IF NOT EXISTS merchants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    business_name VARCHAR(255) NOT NULL COMMENT '商家名稱',
    business_type VARCHAR(100) COMMENT '商家類型',
    address TEXT COMMENT '商家地址',
    description TEXT COMMENT '商家描述',
    logo_url VARCHAR(500) COMMENT '商家 Logo',
    is_verified BOOLEAN DEFAULT FALSE COMMENT '是否已驗證',
    rating DECIMAL(3,2) DEFAULT 0.00 COMMENT '評分',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 創建菜單項目表
CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    merchant_id INT NOT NULL,
    name VARCHAR(255) NOT NULL COMMENT '菜品名稱',
    description TEXT COMMENT '菜品描述',
    price DECIMAL(10,2) NOT NULL COMMENT '價格',
    category VARCHAR(100) COMMENT '分類',
    image_url VARCHAR(500) COMMENT '圖片',
    is_available BOOLEAN DEFAULT TRUE COMMENT '是否可用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (merchant_id) REFERENCES merchants(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 創建訂單表
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL COMMENT '顧客 ID',
    merchant_id INT NOT NULL COMMENT '商家 ID',
    order_number VARCHAR(50) UNIQUE NOT NULL COMMENT '訂單編號',
    status ENUM('pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled') DEFAULT 'pending' COMMENT '訂單狀態',
    total_amount DECIMAL(10,2) NOT NULL COMMENT '總金額',
    note TEXT COMMENT '備註',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (merchant_id) REFERENCES merchants(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 創建訂單項目表
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1 COMMENT '數量',
    price DECIMAL(10,2) NOT NULL COMMENT '單價',
    subtotal DECIMAL(10,2) NOT NULL COMMENT '小計',
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 添加索引以提高查詢效率
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_merchant ON orders(merchant_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_menu_items_merchant ON menu_items(merchant_id);
CREATE INDEX IF NOT EXISTS idx_menu_items_category ON menu_items(category);

