from fastapi import APIRouter, Depends

from shared_science.auth import create_api_key
from shared_science.dependencies import get_session, get_current_user
from shared_science.models import User
from shared_science.typing import assert_not_none

api = APIRouter()


@api.get("/me")
def get_me(user: User = Depends(get_current_user)):
    return {"message": "protected api_app endpoint", "current_email": user.email}


@api.get("/api-key")
def create_user_api_key(user: User = Depends(get_current_user), session=Depends(get_session)):
    api_key = create_api_key(assert_not_none(user.id), session)
    return {"api_key": api_key}
