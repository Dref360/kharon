import logging
from typing import Optional, List

import httpx
import names_generator
from fastapi import APIRouter, Depends, HTTPException, Query
from httpx import Response
from pydantic import BaseModel
from sqlmodel import Session, select
from starlette.requests import Request

from kharon import sshutils
from kharon.auth import oauth2_scheme
from kharon.dependencies import get_cluster
from kharon.dependencies import get_session, get_current_user
from kharon.models import User, Cluster
from kharon.models.clusters import ClusterStatus
from kharon.typing import assert_not_none

api = APIRouter()

log = logging.getLogger()


class ConnectionResponse(BaseModel):
    name: str
    public_key: str


@api.get("/connect", summary="Connect a cluster to Kharon.")
def get_connect_daemon(
    request: Request,
    name: Optional[str] = None,  # TODO Probably doesn't need this
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
) -> ConnectionResponse:
    if not token.startswith("ss-"):
        raise HTTPException(400, detail="Daemon can only connect with tokens.")

    is_new_cluster = name in ("", None)
    cluster_name = name if not is_new_cluster else names_generator.generate_name(style="hyphen")

    client_host = assert_not_none(request.client).host
    _, ssh_public_key = sshutils.get_ssh_keys(cluster_name)
    if is_new_cluster:
        log.info(f"New Cluster {cluster_name}")
        # New cluster
        cluster = Cluster(
            creator=user.id,
            name=cluster_name,
            host=client_host,
            status=ClusterStatus.healthy,
            user_read_allow=user.email,
        )
        session.add(cluster)
        session.commit()
    else:
        log.info(f"Existing Cluster: {cluster_name}")
        check_exist = session.exec(
            select(Cluster).where(Cluster.name == name).where(Cluster.creator == user.id)
        ).first()
        if check_exist is None:
            raise HTTPException(404, "Cluster not found")
    return ConnectionResponse(name=cluster_name, public_key=open(ssh_public_key, "r").read())


class ClusterView(BaseModel):
    name: str
    online: bool
    url: str
    description: str = ""
    users: List[str]


class ClusterResponse(BaseModel):
    clusters: List[ClusterView]


@api.get("/list", summary="List clusters created by a user")
def list_clusters(
    user: User = Depends(get_current_user), session: Session = Depends(get_session)
) -> ClusterResponse:
    # TODO Add server the person has access to
    clusters = session.exec(select(Cluster).where(Cluster.creator == user.id)).all()
    return ClusterResponse(
        clusters=[
            ClusterView(
                name=c.name,
                online=c.status == ClusterStatus.healthy,
                url=f"/clusters/{c.name}/",
                description="Http Server",
                users=c.user_read_allow.split(","),
            )
            for c in clusters
        ]
    )


@api.post("/add_user/{cluster_name}", summary="Add user to a cluster")
def add_user_to_cluster(
    email: str = Query(...),
    cluster: Cluster = Depends(get_cluster),
    session: Session = Depends(get_session),
):
    cluster.add_user(email, session)
    return "OK"


@api.api_route(
    "/{cluster_name}/{forward_path:path}",
    methods=["GET", "POST", "PUT", "DELETE"],
    summary="Proxy function",
)
async def reverse_proxy(
    forward_path: str, request: Request, cluster: Cluster = Depends(get_cluster)
):
    key, _ = sshutils.get_ssh_keys(cluster.name)
    ssh_tunnel = sshutils.get_ssh_tunnel(ip=cluster.host, port=2222, private_key=key)
    # Forward the request to the target server
    print("Proxy request", forward_path)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=f"http://127.0.0.1:{ssh_tunnel.local_bind_port}/{forward_path}",
                headers=request.headers,
                content=await request.body(),
            )
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
            )
        except httpx.HTTPError:
            # TODO If the request fails, we should redirect to index.html for client-side routing
            return HTTPException(500)
