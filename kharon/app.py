import logging

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, SQLModel, select

from kharon.auth import create_api_key
from kharon.constants import KHARON_STORAGE, KHR_DEBUG
from kharon.dependencies import engine, get_current_user
from kharon.models import *  # noqa Need this to load models into SQLModel
from kharon.models.clusters import ClusterStatus
from kharon.routers.api import api as app_router
from kharon.routers.api_public import api as public_router
from kharon.routers.auth import app as auth_router
from kharon.routers.cluster import api as cluster_router

log = logging.getLogger()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    if KHR_DEBUG:
        # Creating temp user for debugging
        temp_email = "temp@temp.com"
        with Session(engine) as session:
            if (temp := session.exec(select(User).where(User.email == temp_email)).first()) is None:
                temp = User(email=temp_email)
                session.add(temp)
                session.commit()
                session.refresh(temp)
                cluster = Cluster(
                    creator=temp.id,
                    name="potato-whiskey",
                    host="172.20.128.2",
                    remote_host="localhost",
                    status=ClusterStatus.healthy,
                    user_read_allow=temp.email,
                )
                session.add(cluster)
                session.commit()
            token = create_api_key(temp.id, key_name="temp", session=session)
            print("User:", temp.email)
            print("API Token:", token)


# Setup routers
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=(
        r"http:\/\/.*\.?(localdev.me|localhost):3000"
        if KHR_DEBUG
        else r"https:\/\/.*\.?(kharon.app)"
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(auth_router, prefix="/auth")
app.include_router(app_router, prefix="/app", dependencies=[Depends(get_current_user)])
app.include_router(cluster_router, prefix="/clusters", dependencies=[Depends(get_current_user)])
app.include_router(
    public_router,
    prefix="/public",
)
print("Storage:", KHARON_STORAGE)
for r in app.routes:
    print("Route", dict(methods=r.__dict__.get("methods"), path=r.__dict__["path"]))
