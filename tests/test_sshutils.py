import os
import random
import time

from kharon.sshutils import get_ssh_keys


def test_ssh_key_creation():
    token = f"ss-{random.randint(0, 1000000)}"
    private, public = get_ssh_keys(token)

    assert private.split("/")[-1] == f"{token}.key"
    assert public.split("/")[-1] == f"{token}.key.pub"
    ctime = os.stat(private).st_mtime

    # Doesn't get regenerated
    time.sleep(0.1)
    private, public = get_ssh_keys(token)
    assert ctime == os.stat(private).st_mtime
