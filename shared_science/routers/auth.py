import httpx
from fastapi import APIRouter
from fastapi import Body
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from shared_science.auth import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI

# Google OAuth2 configuration
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

app = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # No token URL


class CodeFlow(BaseModel):
    code: str


@app.post("/google")
async def auth_google(body: CodeFlow = Body(...)):
    """Authentify access code

    Args:
        body (CodeFlow, optional): Auth code

    Returns:
        _type_: _description_
    """
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": body.code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = httpx.post(token_url, data=data)
    tokens = response.json()
    access_token = tokens["access_token"]
    id_tokens = tokens["id_token"]
    user_info = httpx.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    return {**user_info.json(), "access_token": access_token, "id_token": id_tokens}
