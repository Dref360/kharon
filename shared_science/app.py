from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from shared_science.dependencies import get_current_user, engine
from shared_science.models import *  # noqa Need this to load models into SQLModel
from shared_science.routers.api import api as app_router
from shared_science.routers.api_public import api as public_router
from shared_science.routers.auth import app as auth_router


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Setup routers
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(auth_router, prefix="/auth")
app.include_router(app_router, prefix="/app", dependencies=[Depends(get_current_user)])
app.include_router(
    public_router,
    prefix="/public",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
