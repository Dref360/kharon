from typing import Optional

import names_generator
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from starlette.requests import Request

from kharon import sshutils
from kharon.auth import create_api_key, oauth2_scheme
from kharon.dependencies import get_session, get_current_user
from kharon.models import User, Cluster
from kharon.models.clusters import ClusterStatus
from kharon.typing import assert_not_none

api = APIRouter()


@api.get("/me")
def get_me(user: User = Depends(get_current_user)):
    return {"message": "protected api_app endpoint", "current_email": user.email}


@api.post("/api-key")
def create_user_api_key(user: User = Depends(get_current_user), session=Depends(get_session)):
    api_key = create_api_key(assert_not_none(user.id), session)
    return {"api_key": api_key}
