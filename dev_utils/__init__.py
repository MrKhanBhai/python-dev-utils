"""Small, dependency-free utilities for Python developers."""
from .checksum import hash_bytes, hash_file, sha256_file
from .directory_hash import directory_hashes
from .duplicate_finder import find_duplicate_files
from .file_compare import files_are_equal
from .manifest import build_manifest, load_manifest, verify_manifest, write_manifest

__all__ = [
    "build_manifest",
    "directory_hashes",
    "files_are_equal",
    "find_duplicate_files",
    "hash_bytes",
    "hash_file",
    "load_manifest",
    "sha256_file",
    "verify_manifest",
    "write_manifest",
]
