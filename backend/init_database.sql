-- ==========================================
-- 餐廳訂餐系統 - 完整資料庫初始化腳本
-- ==========================================
-- 此腳本會創建所有必要的資料表和索引
-- 執行前請確保已創建資料庫：CREATE DATABASE vue_auth;
-- ==========================================

USE vue_auth;

-- ==========================================
-- 1. 創建用戶表 (users)
-- ==========================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用戶名',
    role ENUM('customer', 'merchant') NOT NULL DEFAULT 'customer' COMMENT '角色：顧客/商家',
    password VARCHAR(255) NULL COMMENT '密碼（OAuth用戶可為空）',
    display_name VARCHAR(100) NULL COMMENT '顯示名稱',
    phone VARCHAR(20) NULL COMMENT '電話號碼',
    email VARCHAR(255) NULL COMMENT '電子郵件',
    line_id VARCHAR(100) NULL UNIQUE COMMENT 'LINE ID（OAuth）',
    google_id VARCHAR(100) NULL UNIQUE COMMENT 'Google ID（OAuth）',
    failed_attempts INT DEFAULT 0 COMMENT '登入失敗次數',
    lockout_until DATETIME NULL COMMENT '帳號鎖定到期時間',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 用戶表索引
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_line_id ON users(line_id);
CREATE INDEX IF NOT EXISTS idx_users_google_id ON users(google_id);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- ==========================================
-- 2. 創建商家表 (merchants)
-- ==========================================
CREATE TABLE IF NOT EXISTS merchants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE COMMENT '關聯的用戶ID',
    business_name VARCHAR(255) NOT NULL COMMENT '商家名稱',
    business_type VARCHAR(100) NULL COMMENT '商家類型（如：中式料理、日式料理）',
    address TEXT NULL COMMENT '商家地址',
    description TEXT NULL COMMENT '商家描述',
    logo_url VARCHAR(500) NULL COMMENT '商家Logo圖片URL',
    is_verified BOOLEAN DEFAULT FALSE COMMENT '是否已驗證',
    rating DECIMAL(3,2) DEFAULT 0.00 COMMENT '評分（0.00-5.00）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==========================================
-- 3. 創建菜單項目表 (menu_items)
-- ==========================================
CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    merchant_id INT NOT NULL COMMENT '商家ID',
    name VARCHAR(255) NOT NULL COMMENT '菜品名稱',
    description TEXT NULL COMMENT '菜品描述',
    price DECIMAL(10,2) NOT NULL COMMENT '價格',
    category VARCHAR(100) NULL COMMENT '分類（如：主餐、飲料、甜點）',
    image_url VARCHAR(500) NULL COMMENT '菜品圖片URL',
    is_available BOOLEAN DEFAULT TRUE COMMENT '是否可用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (merchant_id) REFERENCES merchants(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 菜單項目表索引
CREATE INDEX IF NOT EXISTS idx_menu_items_merchant ON menu_items(merchant_id);
CREATE INDEX IF NOT EXISTS idx_menu_items_category ON menu_items(category);
CREATE INDEX IF NOT EXISTS idx_menu_items_available ON menu_items(is_available);

-- ==========================================
-- 4. 創建訂單表 (orders)
-- ==========================================
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL COMMENT '顧客ID',
    merchant_id INT NOT NULL COMMENT '商家ID',
    order_number VARCHAR(50) UNIQUE NOT NULL COMMENT '訂單編號',
    status ENUM('pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled') 
        DEFAULT 'pending' COMMENT '訂單狀態',
    total_amount DECIMAL(10,2) NOT NULL COMMENT '總金額',
    note TEXT NULL COMMENT '訂單備註',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (merchant_id) REFERENCES merchants(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 訂單表索引
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_merchant ON orders(merchant_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_created ON orders(created_at);

-- ==========================================
-- 5. 創建訂單項目表 (order_items)
-- ==========================================
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL COMMENT '訂單ID',
    menu_item_id INT NOT NULL COMMENT '菜品ID',
    quantity INT NOT NULL DEFAULT 1 COMMENT '數量',
    price DECIMAL(10,2) NOT NULL COMMENT '單價（下單時的價格）',
    subtotal DECIMAL(10,2) NOT NULL COMMENT '小計',
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 訂單項目表索引
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_menu ON order_items(menu_item_id);

-- ==========================================
-- 完成
-- ==========================================
-- 資料庫初始化完成！
-- 您現在可以啟動後端應用程式了。

