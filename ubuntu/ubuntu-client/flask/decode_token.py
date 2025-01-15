import jwt
from flask import request, jsonify

def decode_token(token):
    try:
        decoded = jwt.decode(token, 'cameronnasser', algorithms=['HS256'])
        return jsonify({'role': decoded.get('role')}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 decode_token.py <user_id>")
    else:
        user_id = sys.argv[1]
        decode_token(user_id)

