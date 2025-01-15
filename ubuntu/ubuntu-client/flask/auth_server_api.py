import bcrypt
import jwt
import datetime
from bson import ObjectId
from flask import Flask, request, jsonify, redirect, url_for, session, make_response
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cameronnasser'
app.config["MONGO_URI"] = "mongodb://hepl:heplhepl@localhost:27017/reservationDB?authSource=admin"
mongo = PyMongo(app)

SECRET_KEY = 'cameronnasser'
ALGORITHM = 'HS256'
EXPIRATION_TIME = 3600

def check_password(stored_hash, salt, password):
    return stored_hash.encode('utf-8') == bcrypt.hashpw(password.encode(), salt.encode('utf-8'))

def generate_token(user_id):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=EXPIRATION_TIME)
    user = mongo.db['client'].find_one({"_id": ObjectId(user_id)})
    
    if user:
        role = str(user.get('role', ''))
        token = jwt.encode({
            'user_id': user_id,
            'role': role,
            'exp': expiration
        }, SECRET_KEY, algorithm=ALGORITHM)
        
        mongo.db['client'].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"token": token}}
        )
        
        return token
    else:
        raise ValueError("User not found")

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
            response.headers['X-Redirect-To'] = '/'
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
            user = mongo.db['client'].find_one({"_id": ObjectId(user_id)})
            if user:
                role = str(user.get('role', ''))
                response = make_response(jsonify(role=role), 200)
                response.headers['X-Role'] = role  # Ajouter le rôle dans l'en-tête
                return response
            else:
                return jsonify(message="User not found"), 404
        else:
            return jsonify(message="Invalid or expired token"), 401
    else:
        return jsonify(message="No token provided"), 401

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000, ssl_context=('../../certificates/flask.crt', '../../certificates/flask.key'))
