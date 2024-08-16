from datetime import datetime

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlmodel import Session, select

from kharon.auth import create_api_key, disable_api_key
from kharon.dependencies import get_current_user, get_session
from kharon.models import APIKey, User
from kharon.typing import assert_not_none

api = APIRouter()


@api.get("/me")
def get_me(user: User = Depends(get_current_user)):
    return {"message": "protected api_app endpoint", "current_email": user.email}


class APIKeyViewModel(BaseModel):
    key_name: str
    created_at: datetime


@api.get("/api-key")
def get_keys(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    keys = session.exec(
        select(APIKey).where(APIKey.user_id == user.id).where(APIKey.is_active)
    ).all()
    return [
        APIKeyViewModel(key_name=k.key_name, created_at=assert_not_none(k.created_at)) for k in keys
    ]


@api.post("/api-key")
def create_user_api_key(
    user: User = Depends(get_current_user), key_name: str = Query(...), session=Depends(get_session)
):
    api_key = create_api_key(assert_not_none(user.id), key_name, session)
    return {"api_key": api_key}


@api.delete("/api-key")
def delete_user_api_key(
    user: User = Depends(get_current_user), key_name: str = Query(...), session=Depends(get_session)
):
    disable_api_key(user_id=assert_not_none(user.id), key_name=key_name, session=session)
    return "OK"
