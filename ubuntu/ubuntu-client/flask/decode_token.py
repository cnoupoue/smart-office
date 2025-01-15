import jwt
from flask import Flask, jsonify
from pymongo import MongoClient
import sys

SECRET_KEY = 'cameronnasser'
ALGORITHM = 'HS256'

# Initialisation de l'application Flask
app = Flask(__name__)

# Connexion à MongoDB
client = MongoClient("mongodb://hepl:heplhepl@localhost:27017/reservationDB?authSource=admin")
db = client.reservationDB
clients_collection = db["client"]

def decode_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Retourne simplement un dictionnaire, sans utiliser jsonify ici
        return {'role': decoded.get('role')}, 200
    except jwt.ExpiredSignatureError:
        return {'message': 'Token has expired'}, 401
    except jwt.InvalidTokenError:
        return {'message': 'Invalid token'}, 401

def get_token_from_db(user_email):
    user = clients_collection.find_one({"email": user_email})
    if user and 'token' in user:
        return user['token']
    return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 decode_token.py <user_email>")
    else:
        user_email = sys.argv[1]
        token = get_token_from_db(user_email)
        if token:
            response, status_code = decode_token(token)
            # Affichage du résultat sans Flask context
            print(response)
        else:
            print("Token not found for the given user_email.")

