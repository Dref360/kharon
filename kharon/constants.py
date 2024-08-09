import os

from platformdirs import user_cache_dir

KHARON_STORAGE = os.getenv("KHARON_STORAGE") or user_cache_dir(
    "kharon", "kharon-team", ensure_exists=True
)
