from fastapi import Depends, HTTPException, Query, Path
from sqlalchemy import create_engine
from sqlmodel import Session, select

from kharon.auth import get_user_by_api_key, get_user_from_access_token, oauth2_scheme
from kharon.iam import has_access_to_resource
from kharon.models import User, Cluster
import logging

log = logging.getLogger()

# Setup Database
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
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


def get_cluster(
    cluster_name: str = Path(),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Cluster:
    cluster = session.exec(select(Cluster).where(Cluster.name == cluster_name)).first()
    if cluster is None:
        raise HTTPException(404, "Not Found")
    elif not has_access_to_resource(user.email, cluster):
        raise HTTPException(403, "Forbidden")
    return cluster
