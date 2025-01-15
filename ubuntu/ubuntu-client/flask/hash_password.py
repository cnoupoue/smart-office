import bcrypt
import sys

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt).decode('utf-8')
    return hashed_password, salt.decode('utf-8')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(hash(sys.argv[1]))
    else:
        print('Usage: python hash_password.py <password>')
