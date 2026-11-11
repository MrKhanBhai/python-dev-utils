"""Streaming file and bytes hashing helpers."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Union

PathLike = Union[str, Path]
DEFAULT_CHUNK_SIZE = 64 * 1024


def _validate_chunk_size(chunk_size: int) -> None:
    """Reject invalid read sizes, including bool (an int subclass)."""
    valid_type = isinstance(chunk_size, int) and not isinstance(chunk_size, bool)
    if not valid_type or chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")


def _new_hash(algorithm: str) -> "hashlib._Hash":
    """Create a fixed-length hashlib digest with a consistent public error."""
    try:
        digest = hashlib.new(algorithm)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"unsupported hash algorithm: {algorithm!r}") from exc
    if digest.digest_size == 0:
        raise ValueError(
            f"variable-length hash algorithm is not supported: {algorithm!r}"
        )
    return digest


def hash_bytes(data: bytes, algorithm: str = "sha256") -> str:
    """Return the hexadecimal digest of bytes using a fixed-length hashlib algorithm."""
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    digest = _new_hash(algorithm)
    digest.update(data)
    return digest.hexdigest()


def hash_file(
    file_path: PathLike,
    algorithm: str = "sha256",
    chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> str:
    """Hash a file incrementally; file-system errors propagate to the caller."""
    _validate_chunk_size(chunk_size)
    digest = _new_hash(algorithm)
    with Path(file_path).open("rb") as file:
        for chunk in iter(lambda: file.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_file(file_path: PathLike) -> str:
    """Return a file's SHA-256 checksum (backwards-compatible helper)."""
    return hash_file(file_path, algorithm="sha256")
