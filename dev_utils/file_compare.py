"""Memory-efficient file comparison helpers."""
from __future__ import annotations
from pathlib import Path
from .checksum import DEFAULT_CHUNK_SIZE, PathLike, _validate_chunk_size

def files_are_equal(first: PathLike, second: PathLike,
                    chunk_size: int = DEFAULT_CHUNK_SIZE) -> bool:
    """Return whether two files have identical bytes, using bounded memory."""
    _validate_chunk_size(chunk_size)
    first_path, second_path = Path(first), Path(second)
    if first_path.stat().st_size != second_path.stat().st_size:
        return False
    with first_path.open("rb") as left, second_path.open("rb") as right:
        while True:
            left_chunk, right_chunk = left.read(chunk_size), right.read(chunk_size)
            if left_chunk != right_chunk:
                return False
            if not left_chunk:
                return True
