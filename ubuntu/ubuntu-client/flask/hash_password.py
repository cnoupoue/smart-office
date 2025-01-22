import sys
import bcrypt

def hash_password(password):
    # Génère un salt
    salt = bcrypt.gensalt()
    # Hash le mot de passe avec le salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password, salt

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 hash_password.py <password>")
    else:
        password = sys.argv[1]
        hashed_password, salt = hash_password(password)
        print(f"{hashed_password.decode()} {salt.decode()}")
