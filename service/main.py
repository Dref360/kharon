import json
import os.path
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

import httpx
import typer
from typing_extensions import Annotated

pjoin = os.path.join
HTTP_PORT = 8080


def local_service_healthy():
    try:
        httpx.get(f"http://localhost:{HTTP_PORT}")
        return True
    except httpx.ConnectError:
        return False


def kharon_server_healthy(kharon_server):
    try:
        httpx.get(kharon_server)
        return True
    except httpx.ConnectError:
        return False


@dataclass
class ClusterConfig:
    name: str
    public_key: str


def maybe_load_config(cache) -> Optional[ClusterConfig]:
    cache_path = pjoin(cache, "config.json")
    if os.path.exists(cache_path):
        try:
            return ClusterConfig(**json.load(open(cache_path, "r")))
        except json.JSONDecodeError:
            return None
    return None


def save_config(config: ClusterConfig, cache):
    cache_path = pjoin(cache, "config.json")
    json.dump(asdict(config), open(cache_path, "w"))


def connect_to_daemon(kharon_server: str, api_key: str, cluster_name: Optional[str]):
    return ClusterConfig(
        **httpx.get(
            f"{kharon_server}/clusters/connect?name={cluster_name or ''}",
            headers={"Authorization": f"Bearer {api_key}"},
        ).json()
    )


def append_ssh_key(ssh_public_key):
    key_files = str(Path().home() / ".ssh" / "authorized_keys")
    with open(key_files, "a") as f:
        f.write(ssh_public_key)


def main(
    kharon_server: Annotated[str, typer.Argument(envvar="KHARON_SERVER")],
    api_key: Annotated[str, typer.Argument(envvar="KHARON_API_KEY")],
    cache: Annotated[str, typer.Argument(envvar="KHARON_CACHE")] = "/cache",
):
    if not local_service_healthy():
        raise ValueError(
            f"Unable to connect to local application! "
            f"Please verify that `localhost:{HTTP_PORT}` is accessible."
        )
    if not kharon_server_healthy(kharon_server):
        raise ValueError(
            f"Can't connect to {kharon_server},"
            f" could be a firewall issue in your setup or we're down!"
        )

    cluster_name = None
    if (local_cfg := maybe_load_config(cache)) is not None:
        cluster_name = local_cfg.name
    config = connect_to_daemon(kharon_server, api_key=api_key, cluster_name=cluster_name)
    save_config(config, cache)
    append_ssh_key(config.public_key)

    while True:
        time.sleep(60)
        httpx.post(
            f"{kharon_server}/clusters/health_check/{cluster_name}",
            json={
                "local_service_alive": local_service_healthy(),
                "ssh_service_alive": True,  # TODO Check ssh service
            },
            headers={"Authorization": f"Bearer {api_key}"},
        )


if __name__ == "__main__":
    typer.run(main)
