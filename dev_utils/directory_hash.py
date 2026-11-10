"""Deterministic directory hashing helpers."""
from __future__ import annotations
import os
from pathlib import Path
from .checksum import PathLike, hash_file

def directory_hashes(directory: PathLike, algorithm: str = "sha256",
                     exclude_dirs: tuple[str, ...] = ()) -> dict[str, str]:
    """Return a sorted relative-path-to-digest mapping for regular files.

    Paths use POSIX separators. Symbolic links are not followed. Excluded
    directory names are skipped at every depth. This does not combine files
    into a single directory digest.
    """
    root = Path(directory)
    if not root.is_dir():
        raise NotADirectoryError(str(root))
    result: dict[str, str] = {}
    for current, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(
            name for name in dirs
            if name not in exclude_dirs
            and not (Path(current) / name).is_symlink()
        )
        for name in sorted(names):
            path = Path(current) / name
            if path.is_symlink() or not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            result[relative] = hash_file(path, algorithm=algorithm)
    return dict(sorted(result.items()))
