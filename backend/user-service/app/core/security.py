from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import bcrypt
import os
# Import find_dotenv
from dotenv import load_dotenv, find_dotenv

# Ensure the .env is located correctly up the folder tree
load_dotenv(find_dotenv())

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

# --- MODERN BCRYPT HASHING COMPATIBLE WITH WINDOWS & PYTHON 3.11+ ---

def hash_password(password: str) -> str:
    """Encodes the password string to bytes, hashes it, and returns it as a string."""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_bytes.decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    """Verifies a plain text password against a stored hash string."""
    try:
        return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

# --- JWT TOKEN MANAGEMENT ---

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    # Use modern timezone-aware UTC datetime
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    # Use modern timezone-aware UTC datetime
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    # Note: This will raise JWTError/ExpiredSignatureError if invalid, 
    # which you can catch in your FastAPI route or dependency.
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])