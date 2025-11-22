from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['JWT_ALGORITHM'] = 'HS256'

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

# 取得資料庫連接
def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # 驗證輸入
        if not username or not email or not password:
            return jsonify({'error': '所有欄位都是必填的'}), 400

        if len(password) < 6:
            return jsonify({'error': '密碼長度至少需要 6 個字元'}), 400

        # 檢查用戶是否已存在
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM users WHERE username = %s OR email = %s', (username, email))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': '用戶名或電子郵件已存在'}), 400

        # 建立新用戶
        hashed_password = generate_password_hash(password)
        cursor.execute(
            'INSERT INTO users (username, email, password) VALUES (%s, %s, %s)',
            (username, email, hashed_password)
        )
        conn.commit()
        conn.close()

        return jsonify({'message': '註冊成功'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': '用戶名和密碼都是必填的'}), 400

        # 驗證用戶
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email, password FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        conn.close()

        if not user or not check_password_hash(user['password'], password):
            return jsonify({'error': '用戶名或密碼錯誤'}), 401

        # 建立 JWT token
        access_token = create_access_token(identity=user['id'])

        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email, created_at FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            return jsonify({'error': '用戶不存在'}), 404

        return jsonify({
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'created_at': str(user['created_at']) if user['created_at'] else None
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)

