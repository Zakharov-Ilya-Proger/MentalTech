import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from settings import settings

def create_access_token(data: dict):
    copy_data = data.copy()
    time_now = datetime.now()
    expire = time_now + timedelta(days=30)
    copy_data.update({"exp": expire})
    return jwt.encode(copy_data, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str = Depends(OAuth2PasswordBearer)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")