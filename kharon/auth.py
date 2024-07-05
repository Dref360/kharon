import hashlib
import os
import secrets
from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlmodel import Session, select

from kharon.models import User, APIKey

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = "http://localhost:3000"  # Update with your redirect URI
ACCESS_TOKEN_EXPIRE_MINUTES = 3600
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # No token URL


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, GOOGLE_CLIENT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_from_access_token(access_token: str, session: Session) -> Optional[User]:
    data = jwt.decode(access_token, GOOGLE_CLIENT_SECRET, algorithms=[ALGORITHM])
    if data["issued_to"] == GOOGLE_CLIENT_ID:
        email = data["email"]
        return session.exec(select(User).where(User.email == email)).first()
    return None


def create_api_key(user_id: int, session: Session) -> str:
    api_key = f"ss-{secrets.token_urlsafe(32)}"
    hashed_key = hash_token(api_key)
    db_api_key = APIKey(hashed_key=hashed_key, user_id=user_id)
    session.add(db_api_key)
    session.commit()
    return api_key


def disable_api_key(api_key: str, session: Session) -> None:
    hashed_key = hash_token(api_key)
    db_api_key = session.exec(select(APIKey).where(APIKey.hashed_key == hashed_key)).first()
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
