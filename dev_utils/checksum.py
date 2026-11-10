
import hashlib
from pathlib import Path


def sha256_file(file_path: str) -> str:
    """Calculate the SHA-256 checksum of a file."""
    path = Path(file_path)
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            digest.update(chunk)

    return digest.hexdigest()
