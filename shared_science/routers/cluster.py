from typing import Optional

import httpx
import names_generator
from fastapi import APIRouter, Depends, HTTPException
from httpx import Response
from pydantic import BaseModel
from sqlmodel import Session, select
from starlette.requests import Request

from shared_science import sshutils
from shared_science.auth import oauth2_scheme
from shared_science.dependencies import get_cluster
from shared_science.dependencies import get_session, get_current_user
from shared_science.models import User, Cluster
from shared_science.models.clusters import ClusterStatus

api = APIRouter()

TARGET_URL = "https://github.com"


class ConnectionResponse(BaseModel):
    name: str
    public_key: str


@api.get("/connect",
         summary="Connect a cluster to SharedScience.")
def get_connect_daemon(request: Request,
                       name: Optional[str] = None,  # TODO Probably doesn't need this
                       user: User = Depends(get_current_user),
                       session: Session = Depends(get_session),
                       token: str = Depends(oauth2_scheme),
                       ) -> ConnectionResponse:
    if not token.startswith('ss-'):
        raise HTTPException(400, detail="Daemon can only connect with tokens.")

    client_host = request.client.host
    _, ssh_public_key = sshutils.get_ssh_keys(token)
    if name is None:
        name = names_generator.generate_name(style='hyphen')
        cluster = Cluster(
            creator=user.id,
            name=name,
            host=client_host,
            status=ClusterStatus.healthy
        )
        session.add(cluster)
        session.commit()
    else:
        cluster = session.exec(select(Cluster).where(Cluster.name == name).where(Cluster.creator == user.id)).first()
        if cluster is None:
            raise HTTPException(404, "Cluster not found")
    return ConnectionResponse(
        name=name,
        public_key=open(ssh_public_key, 'r').read()
    )


@api.api_route("/{cluster_name}/{forward_path:path}", methods=["GET", "POST", "PUT", "DELETE"],
               summary="Proxy function")
async def reverse_proxy(forward_path: str, request: Request, cluster: Cluster = Depends(get_cluster),
                        token: str = Depends(oauth2_scheme)):
    url = f"{TARGET_URL}/{forward_path}"
    key, _ = sshutils.get_ssh_keys(token)
    ssh_tunnel = sshutils.get_ssh_tunnel(ip=cluster.host, port=2222, private_key=key)
    # Forward the request to the target server
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=f'http://127.0.0.1:{ssh_tunnel.local_bind_port}/{forward_path}',
                headers=request.headers,
                content=await request.body()
            )
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.HTTPError:
            # TODO If the request fails, we should redirect to index.html for client-side routing
            return HTTPException(500)
