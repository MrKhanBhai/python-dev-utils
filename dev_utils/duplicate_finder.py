"""Read-only duplicate file discovery."""
from __future__ import annotations
import os
from collections import defaultdict
from pathlib import Path
from .checksum import PathLike, hash_file

def find_duplicate_files(directory: PathLike, recursive: bool = True) -> list[list[Path]]:
    """Return groups of identical files without deleting or modifying anything.

    Files are grouped by size before hashing. Symbolic links are skipped.
    """
    root = Path(directory)
    if not root.is_dir():
        raise NotADirectoryError(str(root))
    candidates: dict[int, list[Path]] = defaultdict(list)
    if recursive:
        for current, dirs, names in os.walk(root, followlinks=False):
            dirs[:] = sorted(d for d in dirs if not (Path(current) / d).is_symlink())
            for name in sorted(names):
                path = Path(current) / name
                if not path.is_symlink() and path.is_file():
                    candidates[path.stat().st_size].append(path)
    else:
        for path in sorted(root.iterdir()):
            if path.is_file() and not path.is_symlink():
                candidates[path.stat().st_size].append(path)
    groups: dict[str, list[Path]] = defaultdict(list)
    for same_size in candidates.values():
        if len(same_size) > 1:
            for path in same_size:
                groups[hash_file(path)].append(path)
    duplicates = [sorted(paths) for paths in groups.values() if len(paths) > 1]
    return sorted(duplicates, key=lambda group: str(group[0]))
