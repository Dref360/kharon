from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from shared_science.routers.api import api as app_router
from shared_science.routers.api_public import api as public_router
from shared_science.routers.auth import app as auth_router, get_user_email_from_token



# Setup routers
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix='/auth')
app.include_router(app_router, prefix='/app', dependencies=[Depends(get_user_email_from_token)])
app.include_router(public_router, prefix='/public', )



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
