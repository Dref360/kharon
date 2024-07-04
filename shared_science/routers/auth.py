import logging

from fastapi import APIRouter, HTTPException, Depends
from fastapi import Body
from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
from pydantic import BaseModel
from sqlmodel import Session

from shared_science import dbutils
from shared_science.auth import GOOGLE_CLIENT_ID, create_access_token
from shared_science.dependencies import get_session
from shared_science.models import User

# Google OAuth2 configuration
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

log = logging.getLogger()
app = APIRouter()


class CodeFlow(BaseModel):
    idToken: str


@app.post("/google")
async def auth_google(body: CodeFlow = Body(...), session: Session = Depends(get_session)):
    """Authentify access code

    Args:
        body (CodeFlow, optional): Auth code

    Returns:
        _type_: _description_
    """
    try:
        idinfo = verify_oauth2_token(body.idToken, requests.Request(), GOOGLE_CLIENT_ID)

        # You should add more checks here, like checking the audience, expiration, etc.
        print(idinfo)
        user_id = idinfo["sub"]

        # Here you would typically:
        # 1. Check if the user exists in your database
        # 2. Create a new user if they don't exist
        if not dbutils.user_exists(email=idinfo["email"], session=session):
            log.info(f"New user! {idinfo['email']}")
            user = User(email=idinfo["email"])
            session.add(user)
            session.commit()

        access_token = create_access_token(
            data={"sub": user_id, "email": idinfo["email"], "issued_to": GOOGLE_CLIENT_ID}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")
