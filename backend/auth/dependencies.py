import os
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..database.models import User

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str, db: Session=Depends(get_db)) -> User:
    """Get the authenticated user from JWT token"""
    credential_exception = HTTPException(status=401, detail="Invalid credentials.", headers={"WWW-Authentication": "Bearer"})
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        user_id = payload.get("sub")
        if user_id is None:
            raise credential_exception
    except jwt.InvalidTokenError:
        raise credential_exception
    user = db.get(User, int(user_id))
    if user is None:
        raise credential_exception
    return user
