-- 更新資料庫結構以支持新的 API 規範
-- 請在執行此腳本前備份資料庫

USE vue_auth;

-- 添加新欄位到 users 表
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS display_name VARCHAR(100) NULL,
ADD COLUMN IF NOT EXISTS line_id VARCHAR(100) NULL UNIQUE,
ADD COLUMN IF NOT EXISTS google_id VARCHAR(100) NULL UNIQUE,
ADD COLUMN IF NOT EXISTS failed_attempts INT DEFAULT 0,
ADD COLUMN IF NOT EXISTS lockout_until DATETIME NULL;

-- 修改 email 欄位為可選（OAuth 用戶可能沒有 email）
ALTER TABLE users MODIFY COLUMN email VARCHAR(100) NULL;

-- 修改 password 欄位為可選（OAuth 用戶可能沒有密碼）
ALTER TABLE users MODIFY COLUMN password VARCHAR(255) NULL;

-- 添加索引以提高查詢效能
CREATE INDEX IF NOT EXISTS idx_line_id ON users(line_id);
CREATE INDEX IF NOT EXISTS idx_google_id ON users(google_id);
CREATE INDEX IF NOT EXISTS idx_username ON users(username);


