import bcrypt
import time
import jwt

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session
from typing import Dict

from settings.settings import settings

from models.user import User
from schemas.user import UserDTO


def encode_pass(password: str) -> str:
    return bytes(password, encoding="utf-8")


def create_user(data: UserDTO, db: Session) -> dict:
    password = encode_pass(data.password)
    hashed_pass = bcrypt.hashpw(password, bcrypt.gensalt())
    user = User(email=data.email, password=hashed_pass.decode())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def check_user(data: UserDTO, db: Session) -> dict:
    user = db.query(User).filter(User.email == data.email).first()
    if user: 
        password = encode_pass(data.password)
        return user if bcrypt.checkpw(password, encode_pass(user.password)) else {}
    else:
        return {}


def token_response(access_token: str, refresh_token: str):
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

    
def signJWT(user_id: str) -> Dict[str, str]:
    access_payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    refresh_payload = {
        "user_id": user_id,
        "expires": time.time() + 3600
    }
     
    access_token = jwt.encode(access_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    refresh_token = jwt.encode(refresh_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    return token_response(access_token, refresh_token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return jwt.decode(credentials.credentials, options={"verify_signature": False})
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


class JWTBearerRefresh(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearerRefresh, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearerRefresh, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return jwt.decode(credentials.credentials, options={"verify_signature": False})
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
