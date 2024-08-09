import logging

from fastapi import APIRouter, HTTPException, Depends
from fastapi import Body
from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
from pydantic import BaseModel
from sqlmodel import Session
from starlette.responses import Response

from kharon import dbutils
from kharon.auth import GOOGLE_CLIENT_ID, create_access_token
from kharon.dependencies import get_session
from kharon.models import User

# Google OAuth2 configuration
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"

log = logging.getLogger()
app = APIRouter()


class CodeFlow(BaseModel):
    idToken: str


@app.post("/google")
async def auth_google(
    response: Response, body: CodeFlow = Body(...), session: Session = Depends(get_session)
):
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

        if not dbutils.user_exists(email=idinfo["email"], session=session):
            log.info(f"New user! {idinfo['email']}")
            user = User(email=idinfo["email"])
            session.add(user)
            session.commit()

        access_token = create_access_token(
            data={"sub": user_id, "email": idinfo["email"], "issued_to": GOOGLE_CLIENT_ID}
        )
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=True,  # Use only with HTTPS
            samesite="none",
            domain="localhost",  # Notice the leading dot
            max_age=24 * 60 * 60,
        )  # 24 hours)
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")


@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="access_token", domain="localhost", secure=False, httponly=True, samesite="none"
    )
    return {"message": "Successfully logged out"}
