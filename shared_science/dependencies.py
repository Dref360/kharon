from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlmodel import Session

from shared_science.auth import get_user_by_api_key, get_user_from_access_token
from shared_science.models import User

# Setup Database
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


def get_current_user(
    token: str = Depends(OAuth2PasswordBearer), session: Session = Depends(get_session)
) -> User:
    if token.startswith("ss-"):
        # API Token
        user = get_user_by_api_key(token, session)
    else:
        # Google Auth
        user = get_user_from_access_token(token, session)
    if user is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return user
