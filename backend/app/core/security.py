from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from pwdlib import PasswordHash
from .config import settings

password_hash = PasswordHash.recommended()
ALGO = "HS256"

def generate_password_hash(password: str):
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime().utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGO)
        return encoded_jwt
