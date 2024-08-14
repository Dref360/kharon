import hashlib
import os
import secrets
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from sqlmodel import Session, select
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from kharon.models import APIKey, User

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
ACCESS_TOKEN_EXPIRE_MINUTES = 3600
ALGORITHM = "HS256"


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.cookies.get("access_token") or request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": scheme},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")  # No token URL


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, GOOGLE_CLIENT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_from_access_token(access_token: str, session: Session) -> Optional[User]:
    data = jwt.decode(access_token, GOOGLE_CLIENT_SECRET, algorithms=[ALGORITHM])
    print(data)
    if data["issued_to"] == GOOGLE_CLIENT_ID:
        email = data["email"]
        return session.exec(select(User).where(User.email == email)).first()
    return None


def create_api_key(user_id: int, key_name: str, session: Session) -> str:
    api_key = f"ss-{secrets.token_urlsafe(32)}"
    hashed_key = hash_token(api_key)
    db_api_key = APIKey(hashed_key=hashed_key, key_name=key_name, user_id=user_id)
    session.add(db_api_key)
    session.commit()
    return api_key


def disable_api_key(user_id: int, key_name: str, session: Session) -> None:
    db_api_key = session.exec(
        select(APIKey).where(APIKey.key_name == key_name).where(APIKey.user_id == user_id)
    ).first()
    if db_api_key and db_api_key.is_active:
        db_api_key.is_active = False
        session.add(db_api_key)
        session.commit()


def get_user_by_api_key(api_key: str, session: Session) -> Optional[User]:
    hashed_key = hash_token(api_key)
    db_api_key = session.exec(select(APIKey).where(APIKey.hashed_key == hashed_key)).first()
    if db_api_key and db_api_key.is_active:
        return session.exec(select(User).where(User.id == db_api_key.user_id)).first()
    return None


def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()
