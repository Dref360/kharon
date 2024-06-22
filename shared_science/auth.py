import hashlib
import os
import secrets
from typing import Optional

import httpx
from sqlmodel import Session, select

from shared_science.models import User, APIKey

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = "http://localhost:3000"  # Update with your redirect URI


def get_user_from_access_token(access_token: str, session: Session) -> Optional[User]:
    data = httpx.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}"
    ).json()
    if data["issued_to"] == GOOGLE_CLIENT_ID:
        email = data["email"]
        return session.exec(select(User).where(User.email == email)).first()
    return None


def create_api_key(user_id: int, session: Session) -> str:
    api_key = f"ss-{secrets.token_urlsafe(32)}"
    hashed_key = hashlib.sha256(api_key.encode()).hexdigest()
    db_api_key = APIKey(hashed_key=hashed_key, user_id=user_id)
    session.add(db_api_key)
    session.commit()
    return api_key


def get_user_by_api_key(api_key: str, session: Session) -> Optional[User]:
    hashed_key = hashlib.sha256(api_key.encode()).hexdigest()
    db_api_key = session.exec(select(APIKey).where(APIKey.hashed_key == hashed_key)).first()
    if db_api_key:
        return session.exec(select(User).where(User.id == db_api_key.user_id)).first()
    return None
