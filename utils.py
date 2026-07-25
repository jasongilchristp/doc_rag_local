"""Small shared helper utilities."""

import os
from config import ALLOWED_EXTENSIONS


def allowed_file(filename: str) -> bool:
    """Check whether a filename has an allowed extension."""
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS