import logging
import os
import subprocess
from typing import Tuple

from platformdirs import user_cache_dir
from sshtunnel import SSHTunnelForwarder

from kharon.auth import hash_token

SSH_USERNAME = "shared"

pjoin = os.path.join
log = logging.getLogger()


def get_ssh_keys(name: str) -> Tuple[str, str]:
    """Get ssh keys for this cluster

    Returns:
        Private and Public key file.
    """
    cachedir = pjoin(user_cache_dir("shared-science", "shared-science"), "sshkey")
    os.makedirs(cachedir, exist_ok=True)
    private_key_file = pjoin(cachedir, f"{name}.key")
    public_key_file = pjoin(cachedir, f"{name}.key.pub")
    if not os.path.exists(public_key_file) or not os.path.exists(private_key_file):
        subprocess.run(["ssh-keygen", "-t", "rsa", "-N", "", "-f", private_key_file], check=True)
    return private_key_file, public_key_file


def get_ssh_tunnel(ip, port, remote_host, private_key) -> SSHTunnelForwarder:
    """Start an SSH Tunnel"""
    cachedir = pjoin(user_cache_dir("shared-science", "shared-science"), "sshkey")
    print(
        dict(
            host=(ip, port),
            ssh_pkey=private_key,
            ssh_private_key_password="",
            ssh_username=SSH_USERNAME,
            host_pkey_directories=cachedir,
            remote_bind_address=(remote_host, 8080),
        )
    )
    server = SSHTunnelForwarder(
        (ip, port),
        ssh_pkey=private_key,
        ssh_private_key_password="",
        ssh_username=SSH_USERNAME,
        host_pkey_directories=cachedir,
        remote_bind_address=(remote_host, 8080),
    )

    server.start()

    log.info(f"New connection at :{server.local_bind_port}")  # show assigned local port
    # work with `SECRET SERVICE` through `server.local_bind_port`.
    return server
