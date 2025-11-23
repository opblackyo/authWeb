from flask import Flask, request, jsonify, redirect, render_template_string
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
import os
import base64
import io
import random
import string
import time
import requests
import json
from datetime import timedelta, datetime
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import jwt as pyjwt
from urllib.parse import quote

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=1800)  # 30 分鐘
app.config['JWT_ALGORITHM'] = 'HS256'

CAPTCHA_SECRET_KEY = os.getenv('CAPTCHA_SECRET_KEY', 'captcha-secret-key-change-in-production')

CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])
jwt = JWTManager(app)

# 資料庫配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'vue_auth'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# OAuth 配置
LINE_CLIENT_ID = os.getenv('LINE_CLIENT_ID', '')
LINE_CLIENT_SECRET = os.getenv('LINE_CLIENT_SECRET', '')
LINE_REDIRECT_URI = os.getenv('LINE_REDIRECT_URI', 'http://localhost:5000/api/callback/line')
LINE_LINK_REDIRECT_URI = os.getenv('LINE_LINK_REDIRECT_URI', 'http://localhost:5000/api/callback/link/line')

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '')
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5000/api/callback/google')
GOOGLE_LINK_REDIRECT_URI = os.getenv('GOOGLE_LINK_REDIRECT_URI', 'http://localhost:5000/api/callback/link/google')

# 取得資料庫連接
def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

# 驗證碼生成器
def generate_captcha_image(text, width=200, height=80):
    """生成驗證碼圖片"""
    # 創建圖片
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # 嘗試載入字體，如果失敗則使用默認字體
    try:
        # Windows 系統字體路徑
        font_path = 'C:/Windows/Fonts/arial.ttf'
        if not os.path.exists(font_path):
            font_path = 'C:/Windows/Fonts/calibri.ttf'
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, 36)
        else:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # 繪製文字
    text_width = sum(draw.textbbox((0, 0), char, font=font)[2] - draw.textbbox((0, 0), char, font=font)[0] for char in text)
    text_height = draw.textbbox((0, 0), text, font=font)[3] - draw.textbbox((0, 0), text, font=font)[1]
    
    x = (width - text_width) / 2
    y = (height - text_height) / 2
    
    # 繪製每個字符，添加隨機偏移和顏色
    char_x = x
    for char in text:
        # 隨機顏色
        color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
        # 隨機偏移
        offset_y = random.randint(-5, 5)
        draw.text((char_x, y + offset_y), char, fill=color, font=font)
        # 獲取字符寬度
        bbox = draw.textbbox((0, 0), char, font=font)
        char_x += (bbox[2] - bbox[0]) + 5
    
    # 添加干擾線
    for _ in range(3):
        start = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([start, end], fill=(random.randint(150, 255), random.randint(150, 255), random.randint(150, 255)), width=2)
    
    # 添加干擾點
    for _ in range(50):
        x_point = random.randint(0, width)
        y_point = random.randint(0, height)
        draw.point((x_point, y_point), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    
    # 轉換為 BytesIO
    img_io = io.BytesIO()
    image.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io

# 驗證碼存儲（實際應用中應使用 Redis 等）
captcha_store = {}

def generate_captcha_token():
    """生成驗證碼 token"""
    return pyjwt.encode(
        {'timestamp': time.time()},
        CAPTCHA_SECRET_KEY,
        algorithm='HS256'
    )

def verify_captcha_token(token, answer):
    """驗證驗證碼"""
    try:
        payload = pyjwt.decode(token, CAPTCHA_SECRET_KEY, algorithms=['HS256'])
        timestamp = payload.get('timestamp', 0)
        
        # 驗證碼 5 分鐘過期
        if time.time() - timestamp > 300:
            return False, '驗證碼已過期'
        
        # 從存儲中獲取答案
        if token not in captcha_store:
            return False, '驗證碼無效'
        
        stored_answer = captcha_store[token]
        # 清理已使用的驗證碼
        del captcha_store[token]
        
        if stored_answer.lower() != answer.lower():
            return False, '驗證碼錯誤'
        
        return True, None
    except Exception as e:
        return False, '驗證碼驗證失敗'

def check_account_lockout(username):
    """檢查帳號是否被鎖定"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # 先檢查欄位是否存在
        cursor.execute("SHOW COLUMNS FROM users LIKE 'lockout_until'")
        has_lockout = cursor.fetchone() is not None
        
        if not has_lockout:
            conn.close()
            return False, None
        
        cursor.execute(
            'SELECT failed_attempts, lockout_until FROM users WHERE username = %s',
            (username,)
        )
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return False, None
        
        if user.get('lockout_until'):
            lockout_time = user['lockout_until']
            if isinstance(lockout_time, datetime):
                if lockout_time > datetime.now():
                    return True, lockout_time
            elif isinstance(lockout_time, str):
                lockout_time = datetime.fromisoformat(lockout_time.replace('Z', '+00:00'))
                if lockout_time > datetime.now():
                    return True, lockout_time
        
        return False, None
    except Exception:
        # 如果發生錯誤（例如欄位不存在），返回未鎖定
        return False, None

def record_failed_login(username):
    """記錄登入失敗"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 檢查欄位是否存在
        cursor.execute("SHOW COLUMNS FROM users LIKE 'failed_attempts'")
        has_failed_attempts = cursor.fetchone() is not None
        
        if not has_failed_attempts:
            conn.close()
            return
        
        cursor.execute(
            'SELECT failed_attempts FROM users WHERE username = %s',
            (username,)
        )
        user = cursor.fetchone()
        
        if user:
            failed_attempts = (user.get('failed_attempts') or 0) + 1
            
            # 5 次失敗後鎖定 30 分鐘
            cursor.execute("SHOW COLUMNS FROM users LIKE 'lockout_until'")
            has_lockout = cursor.fetchone() is not None
            
            if failed_attempts >= 5 and has_lockout:
                lockout_until = datetime.now() + timedelta(minutes=30)
                cursor.execute(
                    'UPDATE users SET failed_attempts = %s, lockout_until = %s WHERE username = %s',
                    (failed_attempts, lockout_until, username)
                )
            else:
                cursor.execute(
                    'UPDATE users SET failed_attempts = %s WHERE username = %s',
                    (failed_attempts, username)
                )
            
            conn.commit()
        
        conn.close()
    except Exception:
        # 如果發生錯誤（例如欄位不存在），忽略
        pass

def reset_failed_attempts(username):
    """重置登入失敗次數"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 檢查欄位是否存在
        cursor.execute("SHOW COLUMNS FROM users LIKE 'failed_attempts'")
        has_failed_attempts = cursor.fetchone() is not None
        
        if not has_failed_attempts:
            conn.close()
            return
        
        cursor.execute("SHOW COLUMNS FROM users LIKE 'lockout_until'")
        has_lockout = cursor.fetchone() is not None
        
        if has_lockout:
            cursor.execute(
                'UPDATE users SET failed_attempts = 0, lockout_until = NULL WHERE username = %s',
                (username,)
            )
        else:
            cursor.execute(
                'UPDATE users SET failed_attempts = 0 WHERE username = %s',
                (username,)
            )
        
        conn.commit()
        conn.close()
    except Exception:
        # 如果發生錯誤（例如欄位不存在），忽略
        pass

# ==================== 驗證碼 API ====================

@app.route('/api/captcha', methods=['GET'])
def get_captcha():
    """取得驗證碼圖片和 token"""
    try:
        # 生成隨機驗證碼文字（4 個字符）
        captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        
        # 生成驗證碼圖片
        image_io = generate_captcha_image(captcha_text)
        
        # 轉換為 base64
        image_bytes = image_io.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        image_data_url = f"data:image/png;base64,{image_base64}"
        
        # 生成 token
        captcha_token = generate_captcha_token()
        
        # 存儲驗證碼答案
        captcha_store[captcha_token] = captcha_text
        
        return jsonify({
            'captcha_token': captcha_token,
            'image': image_data_url
        }), 200
    
    except Exception as e:
        import traceback
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        return jsonify({'error': error_msg}), 500

# ==================== 身份驗證 API ====================

@app.route('/api/register', methods=['POST'])
def register():
    """註冊新帳號"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        role = data.get('role', 'customer')  # 新增：角色欄位，默認為顧客
        display_name = data.get('display_name', '')  # 新增：顯示名稱
        email = data.get('email', '')  # 新增：電子郵件
        phone = data.get('phone', '')  # 新增：電話號碼

        # 驗證輸入
        if not username or not password or not confirm_password:
            return jsonify({'message': '所有欄位都是必填的'}), 400

        # 驗證角色
        if role not in ['customer', 'merchant']:
            return jsonify({'message': '無效的角色類型'}), 400

        # 驗證密碼長度
        if len(password) < 6:
            return jsonify({'message': '密碼長度至少需要 6 個字元'}), 400

        # 驗證使用者名稱長度
        if len(username) < 4:
            return jsonify({'message': '使用者名稱至少需要 4 個字元'}), 400

        # 驗證密碼一致性
        if password != confirm_password:
            return jsonify({'message': '兩次密碼輸入不一致'}), 400

        # 檢查用戶是否已存在
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'message': '此帳號已被註冊'}), 409

        # 如果提供了 email，檢查是否已被使用
        if email:
            cursor.execute('SELECT id FROM users WHERE email = %s', (email,))
            if cursor.fetchone():
                conn.close()
                return jsonify({'message': '此電子郵件已被使用'}), 409

        # 建立新用戶
        hashed_password = generate_password_hash(password)

        # 檢查資料表結構
        cursor.execute("SHOW COLUMNS FROM users LIKE 'role'")
        has_role = cursor.fetchone() is not None
        cursor.execute("SHOW COLUMNS FROM users LIKE 'failed_attempts'")
        has_failed_attempts = cursor.fetchone() is not None

        # 根據資料表結構插入數據
        if has_role and has_failed_attempts:
            # 新版資料庫：有 role 和 failed_attempts 欄位
            cursor.execute(
                '''INSERT INTO users (username, role, password, display_name, email, phone, failed_attempts)
                   VALUES (%s, %s, %s, %s, %s, %s, 0)''',
                (username, role, hashed_password, display_name or username, email, phone)
            )
        elif has_role:
            # 有 role 但沒有 failed_attempts
            cursor.execute(
                '''INSERT INTO users (username, role, password, display_name, email, phone)
                   VALUES (%s, %s, %s, %s, %s, %s)''',
                (username, role, hashed_password, display_name or username, email, phone)
            )
        elif has_failed_attempts:
            # 舊版資料庫：只有 failed_attempts
            cursor.execute(
                'INSERT INTO users (username, password, failed_attempts) VALUES (%s, %s, 0)',
                (username, hashed_password)
            )
        else:
            # 最舊版資料庫：只有基本欄位
            cursor.execute(
                'INSERT INTO users (username, password) VALUES (%s, %s)',
                (username, hashed_password)
            )

        user_id = cursor.lastrowid

        # 如果是商家，創建商家資料
        if role == 'merchant' and has_role:
            business_name = data.get('business_name', display_name or username)
            cursor.execute(
                '''INSERT INTO merchants (user_id, business_name) VALUES (%s, %s)''',
                (user_id, business_name)
            )

        conn.commit()
        conn.close()

        return jsonify({
            'message': '註冊成功',
            'username': username,
            'role': role
        }), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """使用者帳號密碼登入"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        captcha_answer = data.get('captcha_answer')
        captcha_token = data.get('captcha_token')
        
        if not username or not password:
            return jsonify({'message': '用戶名和密碼都是必填的'}), 400
        
        if not captcha_answer or not captcha_token:
            return jsonify({'message': '請輸入驗證碼'}), 400
        
        # 驗證驗證碼
        is_valid, error_msg = verify_captcha_token(captcha_token, captcha_answer)
        if not is_valid:
            return jsonify({'message': error_msg or '驗證碼錯誤'}), 400
        
        # 檢查帳號鎖定
        is_locked, lockout_until = check_account_lockout(username)
        if is_locked:
            return jsonify({
                'message': f'帳號因錯誤次數過多被鎖定，請於 {lockout_until.strftime("%Y-%m-%d %H:%M:%S")} 後再試'
            }), 403
        
        # 驗證用戶
        conn = get_db_connection()
        cursor = conn.cursor()

        # 檢查是否有 role 欄位
        cursor.execute("SHOW COLUMNS FROM users LIKE 'role'")
        has_role = cursor.fetchone() is not None

        if has_role:
            cursor.execute(
                'SELECT id, username, email, password, display_name, role, phone, line_id, google_id FROM users WHERE username = %s',
                (username,)
            )
        else:
            cursor.execute(
                'SELECT id, username, email, password, display_name, line_id, google_id FROM users WHERE username = %s',
                (username,)
            )

        user = cursor.fetchone()

        if not user or not user.get('password') or not check_password_hash(user['password'], password):
            conn.close()
            record_failed_login(username)
            return jsonify({'message': '帳號或密碼錯誤'}), 401

        # 如果是商家，獲取商家資訊
        merchant_info = None
        if has_role and user.get('role') == 'merchant':
            cursor.execute(
                'SELECT id, business_name, business_type, address, logo_url, is_verified, rating FROM merchants WHERE user_id = %s',
                (user['id'],)
            )
            merchant_info = cursor.fetchone()

        conn.close()

        # 重置失敗次數
        reset_failed_attempts(username)

        # 建立 JWT token
        access_token = create_access_token(identity=user['id'])

        response_data = {
            'message': '登入成功',
            'token': access_token,
            'user': user['username'],
            'role': user.get('role', 'customer') if has_role else 'customer',
            'display_name': user.get('display_name'),
            'email': user.get('email'),
            'phone': user.get('phone'),
            'expires_in': 1800
        }

        # 如果是商家，添加商家資訊
        if merchant_info:
            response_data['merchant'] = {
                'id': merchant_info['id'],
                'business_name': merchant_info['business_name'],
                'business_type': merchant_info.get('business_type'),
                'address': merchant_info.get('address'),
                'logo_url': merchant_info.get('logo_url'),
                'is_verified': bool(merchant_info.get('is_verified')),
                'rating': float(merchant_info.get('rating', 0))
            }

        return jsonify(response_data), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# ==================== 帳號管理 API ====================

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """取得當前登入使用者的個人資料"""
    try:
        user_id = get_jwt_identity()

        conn = get_db_connection()
        cursor = conn.cursor()

        # 檢查是否有 role 欄位
        cursor.execute("SHOW COLUMNS FROM users LIKE 'role'")
        has_role = cursor.fetchone() is not None

        if has_role:
            cursor.execute(
                'SELECT id, username, email, display_name, role, phone, line_id, google_id FROM users WHERE id = %s',
                (user_id,)
            )
        else:
            cursor.execute(
                'SELECT id, username, email, display_name, line_id, google_id FROM users WHERE id = %s',
                (user_id,)
            )

        user = cursor.fetchone()

        if not user:
            conn.close()
            return jsonify({'message': '用戶不存在'}), 404

        response_data = {
            'message': 'test success',
            'user_id': user['id'],
            'username': user['username'],
            'email': user.get('email'),
            'display_name': user.get('display_name'),
            'role': user.get('role', 'customer') if has_role else 'customer',
            'phone': user.get('phone'),
            'is_line_linked': bool(user.get('line_id')),
            'is_google_linked': bool(user.get('google_id'))
        }

        # 如果是商家，獲取商家資訊
        if has_role and user.get('role') == 'merchant':
            cursor.execute(
                'SELECT id, business_name, business_type, address, description, logo_url, is_verified, rating FROM merchants WHERE user_id = %s',
                (user_id,)
            )
            merchant_info = cursor.fetchone()
            if merchant_info:
                response_data['merchant'] = {
                    'id': merchant_info['id'],
                    'business_name': merchant_info['business_name'],
                    'business_type': merchant_info.get('business_type'),
                    'address': merchant_info.get('address'),
                    'description': merchant_info.get('description'),
                    'logo_url': merchant_info.get('logo_url'),
                    'is_verified': bool(merchant_info.get('is_verified')),
                    'rating': float(merchant_info.get('rating', 0))
                }

        conn.close()
        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/user/username', methods=['POST'])
@jwt_required()
def change_username():
    """變更使用者名稱"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        new_username = data.get('new_username')
        
        if not new_username:
            return jsonify({'message': '新使用者名稱不能為空'}), 400
        
        if len(new_username) < 4:
            return jsonify({'message': '使用者名稱至少需要 4 個字元'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 檢查新使用者名稱是否已被使用
        cursor.execute('SELECT id FROM users WHERE username = %s AND id != %s', (new_username, user_id))
        if cursor.fetchone():
            conn.close()
            return jsonify({'message': '此使用者名稱已被使用'}), 409
        
        # 更新使用者名稱
        cursor.execute('UPDATE users SET username = %s WHERE id = %s', (new_username, user_id))
        conn.commit()
        conn.close()
        
        # 生成新的 JWT token
        new_token = create_access_token(identity=user_id)
        
        return jsonify({
            'message': '使用者名稱變更成功',
            'new_username': new_username,
            'token': new_token,
            'expires_in': 1800
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/user/password', methods=['POST'])
@jwt_required()
def change_password():
    """變更帳號密碼"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        if not old_password or not new_password or not confirm_password:
            return jsonify({'message': '所有欄位都是必填的'}), 400
        
        if len(new_password) < 6:
            return jsonify({'message': '新密碼長度至少需要 6 個字元'}), 400
        
        if new_password != confirm_password:
            return jsonify({'message': '兩次新密碼輸入不一致'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return jsonify({'message': '用戶不存在'}), 404
        
        # 檢查是否有設定密碼（OAuth 用戶可能沒有密碼）
        if not user.get('password'):
            conn.close()
            return jsonify({'message': '第三方登入帳號未設定密碼'}), 401
        
        # 驗證舊密碼
        if not check_password_hash(user['password'], old_password):
            conn.close()
            return jsonify({'message': '舊密碼錯誤'}), 401
        
        # 更新密碼
        hashed_password = generate_password_hash(new_password)
        cursor.execute('UPDATE users SET password = %s WHERE id = %s', (hashed_password, user_id))
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': '密碼變更成功'
        }), 200
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# ==================== OAuth 登入/註冊 API ====================

@app.route('/api/login/line/init', methods=['GET'])
def line_login_init():
    """初始化 LINE 登入/註冊流程"""
    if not LINE_CLIENT_ID:
        return jsonify({'message': 'LINE OAuth 未配置'}), 500
    
    state = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    auth_url = (
        f"https://access.line.me/oauth2/v2.1/authorize?"
        f"response_type=code&"
        f"client_id={LINE_CLIENT_ID}&"
        f"redirect_uri={LINE_REDIRECT_URI}&"
        f"state={state}&"
        f"scope=profile%20openid%20email"
    )
    
    return jsonify({'auth_url': auth_url}), 200

@app.route('/api/login/google/init', methods=['GET'])
def google_login_init():
    """初始化 Google 登入/註冊流程"""
    if not GOOGLE_CLIENT_ID:
        return jsonify({'message': 'Google OAuth 未配置'}), 500
    
    state = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"response_type=code&"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={GOOGLE_REDIRECT_URI}&"
        f"state={state}&"
        f"scope=openid%20profile%20email"
    )
    
    return jsonify({'auth_url': auth_url}), 200

@app.route('/api/callback/line', methods=['GET'])
def line_callback():
    """LINE OAuth 回調"""
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        return render_template_string('''
            <html><body>
                <h1>LINE 登入失敗</h1>
                <p>{{ error }}</p>
            </body></html>
        ''', error=error), 400
    
    if not code:
        return render_template_string('''
            <html><body>
                <h1>LINE 登入失敗</h1>
                <p>未收到授權碼</p>
            </body></html>
        '''), 400
    
    try:
        # 交換 access token
        token_url = 'https://api.line.me/oauth2/v2.1/token'
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': LINE_REDIRECT_URI,
            'client_id': LINE_CLIENT_ID,
            'client_secret': LINE_CLIENT_SECRET
        }
        
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()
        
        if 'access_token' not in token_json:
            return render_template_string('''
                <html><body>
                    <h1>LINE 登入失敗</h1>
                    <p>無法取得 access token</p>
                </body></html>
            '''), 400
        
        access_token = token_json['access_token']
        id_token = token_json.get('id_token')
        
        # 取得用戶資訊
        line_id = None
        email = None
        display_name = ''
        
        if id_token:
            # 嘗試解析 id_token 獲取用戶資訊
            try:
                payload = id_token.split('.')[1]
                payload += '=' * (4 - len(payload) % 4)  # Padding
                decoded_payload = base64.b64decode(payload)
                # 嘗試多種編碼方式
                try:
                    user_info_str = decoded_payload.decode('utf-8')
                except UnicodeDecodeError:
                    # 如果 UTF-8 失敗，嘗試使用 errors='ignore' 或 'replace'
                    user_info_str = decoded_payload.decode('utf-8', errors='replace')
                
                user_info = json.loads(user_info_str)
                line_id = user_info.get('sub')
                email = user_info.get('email')
                display_name = user_info.get('name', '')
                # 確保 display_name 是字符串且可以安全編碼
                if display_name and not isinstance(display_name, str):
                    display_name = str(display_name)
            except (UnicodeDecodeError, json.JSONDecodeError, IndexError, Exception) as e:
                # 如果 id_token 解析失敗，使用 access token 作為備用方法
                # 不拋出異常，而是繼續使用 access token 方法
                pass
        
        # 如果 id_token 解析失敗或沒有 id_token，使用 access token 獲取用戶資訊
        if not line_id:
            profile_url = 'https://api.line.me/v2/profile'
            headers = {'Authorization': f'Bearer {access_token}'}
            profile_response = requests.get(profile_url, headers=headers)
            profile_data = profile_response.json()
            line_id = profile_data.get('userId')
            display_name = profile_data.get('displayName', '')
            if display_name and not isinstance(display_name, str):
                display_name = str(display_name)
            email = None
        
        # 查找或創建用戶
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 檢查是否已有此 LINE ID 的用戶
        cursor.execute('SELECT id, username FROM users WHERE line_id = %s', (line_id,))
        user = cursor.fetchone()
        
        if user:
            # 登入現有用戶
            user_id = user['id']
        else:
            # 創建新用戶
            username = f"line_{line_id[:8]}"
            cursor.execute(
                'INSERT INTO users (username, line_id, display_name, email) VALUES (%s, %s, %s, %s)',
                (username, line_id, display_name, email)
            )
            conn.commit()
            user_id = cursor.lastrowid
        
        conn.close()
        
        # 生成 JWT token
        access_token_jwt = create_access_token(identity=user_id)
        
        # 獲取用戶名
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        # 重定向到前端 OAuth 回調頁面，並在 URL 中傳遞 token
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
        username = user['username'] if user else ''
        # 使用 quote 編碼 URL 參數，避免特殊字符導致編碼錯誤
        redirect_url = f"{frontend_url}/oauth/callback?token={quote(access_token_jwt)}&user={quote(username)}&provider=line"
        return redirect(redirect_url)
    
    except Exception as e:
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
        # 安全地處理錯誤訊息，避免編碼問題
        try:
            error_msg = str(e)
            # 嘗試編碼為 UTF-8，如果失敗則使用簡化訊息
            error_msg.encode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            error_msg = '登入過程中發生錯誤，請重試'
        # 編碼錯誤訊息
        redirect_url = f"{frontend_url}/oauth/callback?error={quote(error_msg, safe='')}&provider=line"
        return redirect(redirect_url)

@app.route('/api/callback/google', methods=['GET'])
def google_callback():
    """Google OAuth 回調"""
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        return render_template_string('''
            <html><body>
                <h1>Google 登入失敗</h1>
                <p>{{ error }}</p>
            </body></html>
        ''', error=error), 400
    
    if not code:
        return render_template_string('''
            <html><body>
                <h1>Google 登入失敗</h1>
                <p>未收到授權碼</p>
            </body></html>
        '''), 400
    
    try:
        # 交換 access token
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'code': code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()
        
        if 'access_token' not in token_json:
            return render_template_string('''
                <html><body>
                    <h1>Google 登入失敗</h1>
                    <p>無法取得 access token</p>
                </body></html>
            '''), 400
        
        access_token = token_json['access_token']
        
        # 取得用戶資訊
        userinfo_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        userinfo_response = requests.get(userinfo_url, headers=headers)
        userinfo_data = userinfo_response.json()
        
        google_id = userinfo_data.get('id')
        email = userinfo_data.get('email')
        display_name = userinfo_data.get('name')
        
        # 查找或創建用戶
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 檢查是否已有此 Google ID 的用戶
        cursor.execute('SELECT id, username FROM users WHERE google_id = %s', (google_id,))
        user = cursor.fetchone()
        
        if user:
            # 登入現有用戶
            user_id = user['id']
        else:
            # 創建新用戶
            username = f"google_{google_id[:8]}"
            cursor.execute(
                'INSERT INTO users (username, google_id, display_name, email) VALUES (%s, %s, %s, %s)',
                (username, google_id, display_name, email)
            )
            conn.commit()
            user_id = cursor.lastrowid
        
        conn.close()
        
        # 生成 JWT token
        access_token_jwt = create_access_token(identity=user_id)
        
        # 獲取用戶名
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        # 重定向到前端 OAuth 回調頁面，並在 URL 中傳遞 token
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
        username = user['username'] if user else ''
        # 使用 quote 編碼 URL 參數，避免特殊字符導致編碼錯誤
        redirect_url = f"{frontend_url}/oauth/callback?token={quote(access_token_jwt)}&user={quote(username)}&provider=google"
        return redirect(redirect_url)
    
    except Exception as e:
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
        error_msg = str(e)
        # 編碼錯誤訊息
        redirect_url = f"{frontend_url}/oauth/callback?error={quote(error_msg)}&provider=google"
        return redirect(redirect_url)

# ==================== OAuth 綁定 API ====================

@app.route('/api/link/line/init', methods=['GET'])
@jwt_required()
def line_link_init():
    """初始化 LINE 帳號綁定流程"""
    if not LINE_CLIENT_ID:
        return jsonify({'message': 'LINE OAuth 未配置'}), 500
    
    user_id = get_jwt_identity()
    # 使用 JWT 編碼 user_id 到 state 中
    state_token = pyjwt.encode({'user_id': user_id, 'type': 'link'}, CAPTCHA_SECRET_KEY, algorithm='HS256')
    auth_url = (
        f"https://access.line.me/oauth2/v2.1/authorize?"
        f"response_type=code&"
        f"client_id={LINE_CLIENT_ID}&"
        f"redirect_uri={LINE_LINK_REDIRECT_URI}&"
        f"state={state_token}&"
        f"scope=profile%20openid%20email"
    )
    
    return jsonify({
        'message': '請導向此 URL 進行 LINE 綁定',
        'auth_url': auth_url
    }), 200

@app.route('/api/link/google/init', methods=['GET'])
@jwt_required()
def google_link_init():
    """初始化 Google 帳號綁定流程"""
    if not GOOGLE_CLIENT_ID:
        return jsonify({'message': 'Google OAuth 未配置'}), 500
    
    user_id = get_jwt_identity()
    # 使用 JWT 編碼 user_id 到 state 中
    state_token = pyjwt.encode({'user_id': user_id, 'type': 'link'}, CAPTCHA_SECRET_KEY, algorithm='HS256')
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"response_type=code&"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={GOOGLE_LINK_REDIRECT_URI}&"
        f"state={state_token}&"
        f"scope=openid%20profile%20email"
    )
    
    return jsonify({
        'message': '請導向此 URL 進行 Google 綁定',
        'auth_url': auth_url
    }), 200

@app.route('/api/callback/link/line', methods=['GET'])
def line_link_callback():
    """LINE OAuth 綁定回調"""
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')
    
    if error:
        return render_template_string('''
            <html><body>
                <h1>LINE 連結失敗</h1>
                <p>{{ error }}</p>
            </body></html>
        ''', error=error), 400
    
    if not code or not state:
        return render_template_string('''
            <html><body>
                <h1>LINE 連結失敗</h1>
                <p>未收到授權碼或狀態參數</p>
            </body></html>
        '''), 400
    
    try:
        # 解析 state 獲取用戶 ID
        state_data = pyjwt.decode(state, CAPTCHA_SECRET_KEY, algorithms=['HS256'])
        user_id = state_data.get('user_id')
        
        if not user_id:
            return render_template_string('''
                <html><body>
                    <h1>LINE 連結失敗</h1>
                    <p>無效的狀態參數</p>
                </body></html>
            '''), 400
        
        # 交換 access token
        token_url = 'https://api.line.me/oauth2/v2.1/token'
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': LINE_LINK_REDIRECT_URI,
            'client_id': LINE_CLIENT_ID,
            'client_secret': LINE_CLIENT_SECRET
        }
        
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()
        
        if 'access_token' not in token_json:
            return render_template_string('''
                <html><body>
                    <h1>LINE 連結失敗</h1>
                    <p>無法取得 access token</p>
                </body></html>
            '''), 400
        
        access_token = token_json['access_token']
        id_token = token_json.get('id_token')
        
        # 取得用戶資訊
        if id_token:
            payload = id_token.split('.')[1]
            payload += '=' * (4 - len(payload) % 4)
            user_info = json.loads(base64.b64decode(payload))
            line_id = user_info.get('sub')
        else:
            profile_url = 'https://api.line.me/v2/profile'
            headers = {'Authorization': f'Bearer {access_token}'}
            profile_response = requests.get(profile_url, headers=headers)
            profile_data = profile_response.json()
            line_id = profile_data.get('userId')
        
        # 檢查此 LINE ID 是否已被其他用戶綁定
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM users WHERE line_id = %s AND id != %s', (line_id, user_id))
        if cursor.fetchone():
            conn.close()
            return render_template_string('''
                <html><body>
                    <h1>LINE 連結失敗</h1>
                    <p>此 LINE 帳號已被其他用戶綁定</p>
                </body></html>
            '''), 409
        
        # 更新用戶的 LINE ID
        cursor.execute('UPDATE users SET line_id = %s WHERE id = %s', (line_id, user_id))
        conn.commit()
        conn.close()
        
        # 返回 JSON 格式（規範要求）
        response_data = {
            'message': '帳號連結成功',
            'is_linked': True
        }
        
        return render_template_string('''
            <html><body>
                <h1>帳號連結成功</h1>
                <pre style="background:#f5f5f5;padding:20px;border-radius:8px;">{{ json_data }}</pre>
                <p>LINE 帳號已成功綁定</p>
                <script>
                    setTimeout(() => {
                        window.close();
                    }, 2000);
                </script>
            </body></html>
        ''', json_data=json.dumps(response_data, ensure_ascii=False, indent=2)), 200
    
    except Exception as e:
        return render_template_string('''
            <html><body>
                <h1>LINE 連結失敗</h1>
                <p>{{ error }}</p>
            </body></html>
        ''', error=str(e)), 500

@app.route('/api/callback/link/google', methods=['GET'])
def google_link_callback():
    """Google OAuth 綁定回調"""
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')
    
    if error:
        return render_template_string('''
            <html><body>
                <h1>Google 連結失敗</h1>
                <p>{{ error }}</p>
            </body></html>
        ''', error=error), 400
    
    if not code or not state:
        return render_template_string('''
            <html><body>
                <h1>Google 連結失敗</h1>
                <p>未收到授權碼或狀態參數</p>
            </body></html>
        '''), 400
    
    try:
        # 解析 state 獲取用戶 ID
        state_data = pyjwt.decode(state, CAPTCHA_SECRET_KEY, algorithms=['HS256'])
        user_id = state_data.get('user_id')
        
        if not user_id:
            return render_template_string('''
                <html><body>
                    <h1>Google 連結失敗</h1>
                    <p>無效的狀態參數</p>
                </body></html>
            '''), 400
        
        # 交換 access token
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'code': code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': GOOGLE_LINK_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()
        
        if 'access_token' not in token_json:
            return render_template_string('''
                <html><body>
                    <h1>Google 連結失敗</h1>
                    <p>無法取得 access token</p>
                </body></html>
            '''), 400
        
        access_token = token_json['access_token']
        
        # 取得用戶資訊
        userinfo_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        userinfo_response = requests.get(userinfo_url, headers=headers)
        userinfo_data = userinfo_response.json()
        
        google_id = userinfo_data.get('id')
        
        # 檢查此 Google ID 是否已被其他用戶綁定
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM users WHERE google_id = %s AND id != %s', (google_id, user_id))
        if cursor.fetchone():
            conn.close()
            return render_template_string('''
                <html><body>
                    <h1>Google 連結失敗</h1>
                    <p>此 Google 帳號已被其他用戶綁定</p>
                </body></html>
            '''), 409
        
        # 更新用戶的 Google ID
        cursor.execute('UPDATE users SET google_id = %s WHERE id = %s', (google_id, user_id))
        conn.commit()
        conn.close()
        
        # 返回 JSON 格式（規範要求）
        response_data = {
            'message': '帳號連結成功',
            'is_linked': True
        }
        
        return render_template_string('''
            <html><body>
                <h1>帳號連結成功</h1>
                <pre style="background:#f5f5f5;padding:20px;border-radius:8px;">{{ json_data }}</pre>
                <p>Google 帳號已成功綁定</p>
                <script>
                    setTimeout(() => {
                        window.close();
                    }, 2000);
                </script>
            </body></html>
        ''', json_data=json.dumps(response_data, ensure_ascii=False, indent=2)), 200
    
    except Exception as e:
        return render_template_string('''
            <html><body>
                <h1>Google 連結失敗</h1>
                <p>{{ error }}</p>
            </body></html>
        ''', error=str(e)), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
