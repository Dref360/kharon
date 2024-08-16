import json
import os.path
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from pprint import pprint
from rich.console import Console
from rich.table import Table
from typing import Optional

import httpx
import typer
from typing_extensions import Annotated

pjoin = os.path.join
HTTP_PORT = 8080
HEALTHY = "Healthy ✅"
NOT_HEALTHY = "Unhealthy ❌"


def local_service_healthy(remote_host):
    try:
        httpx.get(f"http://{remote_host}:{HTTP_PORT}")
        return True
    except httpx.ConnectError as e:
        print(e)
        return False


def kharon_server_healthy(kharon_server):
    try:
        # Give larger timeout
        httpx.get(kharon_server, timeout=10.0)
        return True
    except httpx.ConnectError as e:
        print(e)
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


def connect_to_daemon(
    kharon_server: str, remote_host: str, api_key: str, cluster_name: Optional[str]
) -> ClusterConfig:
    """Connect Daemon to Kharon Backnd

    Args:
        kharon_server : URL of Kharon Backend
        remote_host (str): URL of the local HTTP Server
        api_key (str): Your stored KHARON_API_KEY
        cluster_name (Optional[str]): If this is a restart, supply the name of the clusters.

    Returns:
        ClusterConfig, the current config.
    """
    response = httpx.get(
        f"{kharon_server}/clusters/connect?name={cluster_name or ''}&remote_host={remote_host}",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    if response.status_code == 404 and cluster_name is not None:
        # Need a new name unfortunatly. Something is missing from db.
        response = httpx.get(
            f"{kharon_server}/clusters/connect?remote_host={remote_host}",
            headers={"Authorization": f"Bearer {api_key}"},
        )
    return ClusterConfig(**response.json())


def check_ssh_service():
    # TODO, I don't know if this can fail or how to look at it.
    return True


def append_ssh_key(ssh_public_key: str):
    """Append SSH Key to `authorized_keys`

    Args:
        ssh_public_key: Public key to add

    Notes:
        This always append, it doesn't look for duplicates.
    """
    key_files = str(Path().home() / ".ssh" / "authorized_keys")
    with open(key_files, "a") as f:
        f.write(ssh_public_key)


def main(
    kharon_server: Annotated[str, typer.Argument(envvar="KHARON_SERVER")],
    api_key: Annotated[str, typer.Argument(envvar="KHARON_API_KEY")],
    cache: Annotated[str, typer.Argument(envvar="KHARON_CACHE")] = "/cache",
    remote_host: Annotated[str, typer.Argument(envvar="KHARON_REMOTE_HOST")] = "localhost",
):
    local_service_status = local_service_healthy(remote_host)
    kharon_server_status = kharon_server_healthy(kharon_server)
    console = Console()

    # Create and display the initial table
    table = Table(title="Service Statuses")
    table.add_column("Service", justify="left")
    table.add_column("Status", justify="left")

    # Add initial rows
    table.add_row(
        f"Local Service ({remote_host})", HEALTHY if local_service_status else NOT_HEALTHY
    )
    table.add_row(
        f"Kharon Server ({kharon_server})", HEALTHY if kharon_server_status else NOT_HEALTHY
    )
    table.add_row("Local SSH Server", "Checking...")

    # Print the table
    console.print(table)

    cluster_name = None
    if (local_cfg := maybe_load_config(cache)) is not None:
        cluster_name = local_cfg.name

    config = connect_to_daemon(
        kharon_server, remote_host=remote_host, api_key=api_key, cluster_name=cluster_name
    )
    cluster_name = cluster_name = config.name
    save_config(config, cache)
    append_ssh_key(config.public_key)

    while True:
        # Clear the console to redraw the table
        console.clear()

        # Recheck statuses
        local_service_status = local_service_healthy(remote_host)
        kharon_server_status = kharon_server_healthy(kharon_server)
        ssh_service_status = check_ssh_service()

        # Update table
        table = Table(
            title="Service Statuses",
            caption=f"Access this at https://kharon.app/clusters/{cluster_name}",
        )
        table.add_column("Service", justify="left")
        table.add_column("Status", justify="left")
        table.add_row(
            f"Local Service ({remote_host})", HEALTHY if local_service_status else NOT_HEALTHY
        )
        table.add_row(
            f"Kharon Server ({kharon_server})", HEALTHY if kharon_server_status else NOT_HEALTHY
        )
        table.add_row("Local SSH Server", HEALTHY if ssh_service_status else NOT_HEALTHY)

        # Print the updated table
        console.print(table)

        # Send health check request
        httpx.post(
            f"{kharon_server}/clusters/health_check/{cluster_name}",
            json={
                "local_service_alive": local_service_status,
                "ssh_service_alive": ssh_service_status,
            },
            headers={"Authorization": f"Bearer {api_key}"},
        )

        # Wait for the next update
        time.sleep(60)


if __name__ == "__main__":
    typer.run(main)
