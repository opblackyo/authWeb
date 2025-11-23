-- 快速修復腳本：添加 failed_attempts 和 lockout_until 欄位
-- 如果您在註冊時遇到 "Unknown column 'failed_attempts'" 錯誤，請執行此腳本

USE vue_auth;

-- 添加 failed_attempts 欄位（如果不存在）
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS failed_attempts INT DEFAULT 0 AFTER email;

-- 添加 lockout_until 欄位（如果不存在）
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS lockout_until DATETIME NULL AFTER failed_attempts;

-- 為現有用戶設置預設值
UPDATE users SET failed_attempts = 0 WHERE failed_attempts IS NULL;

-- 顯示更新後的表結構
DESCRIBE users;

