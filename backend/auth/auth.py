from pwdlib import PasswordHash
import os
from datetime import datetime, timedelta, timezone
import jwt

password_hasher = PasswordHash.recommended() # Returns PasswordHash instance with recommended hashers. Current default is Argon2 

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

def hash_password(password: str) -> str:
    return password_hasher.hash(password)
def verify_password(input_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(input_password, hashed_password)

def create_access_token(user_id: int) -> str:
    if not JWT_SECRET_KEY:
        raise RuntimeError("JWT_SECRET_KEY is not set up.")
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expiration_time}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)