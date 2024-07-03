import hashlib
import os
import random
import time

from shared_science.auth import hash_token
from shared_science.sshutils import get_ssh_keys


def test_ssh_key_creation():
    token = f'ss-{random.randint(0, 1000000)}'
    hashed = hash_token(token)
    private, public = get_ssh_keys(token)

    assert private.split('/')[-1] == f"{hashed}.key"
    assert public.split('/')[-1] == f"{hashed}.key.pub"
    ctime = os.stat(private).st_mtime

    # Doesn't get regenerated
    time.sleep(0.1)
    private, public = get_ssh_keys(token)
    assert ctime == os.stat(private).st_mtime
