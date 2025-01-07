import bcrypt
import jwt
import datetime
from flask import Flask, request, jsonify, redirect, url_for, session
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cameronnasser'
app.config["MONGO_URI"] = "mongodb://hepl:heplhepl@localhost:27017/reservationDB?authSource=admin"
mongo = PyMongo(app)

SECRET_KEY = 'cameronnasser'
ALGORITHM = 'HS256'
EXPIRATION_TIME = 3600

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt).decode('utf-8')
    return hashed_password, salt.decode('utf-8')

def check_password(stored_hash, salt, password):
    return stored_hash.encode('utf-8') == bcrypt.hashpw(password.encode(), salt.encode('utf-8'))

def generate_token(user_id):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=EXPIRATION_TIME)
    token = jwt.encode({
        'user_id': user_id,
        'exp': expiration
    }, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/')
def index():
    return jsonify(message="API is working"), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify(message="Email and password are required"), 400
    
    user = mongo.db['client'].find_one({"email": email})
    if user:
        if check_password(user['password'], user['salt'], password):
            token = generate_token(str(user['_id']))
            session['token'] = token
            response = jsonify(message="Login successful", token=token)
            response.headers['X-Redirect-To'] = '/dashboard/'
            return response, 200
        else:
            return jsonify(message="Invalid credentials. Please try again."), 401
    else:
        return jsonify(message="User not found. Please check your email."), 404

@app.route('/validate_token', methods=['GET'])
def validate_token():
    token = session.get('token')
    if token:
        user_id = verify_token(token)
        if user_id:
            return jsonify(message="Token is valid, welcome to the protected area."), 200
        else:
            return jsonify(message="Invalid or expired token"), 401
    else:
        return jsonify(message="No token provided"), 401

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

