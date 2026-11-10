# python-dev-utils

Small, dependency-free file utilities for Python developers.

[![Python versions](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Python:** 3.10+ · **Runtime dependencies:** none · **License:** MIT

## Features

- Stream file contents into a hash using any algorithm supported by `hashlib`.
- Hash in-memory `bytes` without creating a temporary file.
- Compare two files byte-for-byte without reading either file fully into memory.
- Find duplicate files by size and content hash (read-only; never deletes files).
- Generate a deterministic per-file hash manifest for a directory tree.

## Installation

Install the current project directly from GitHub:

```bash
python -m pip install "git+https://github.com/MrKhanBhai/python-dev-utils.git"
```

Or install from a local checkout:

```bash
git clone https://github.com/MrKhanBhai/python-dev-utils.git
cd python-dev-utils
python -m pip install .
```

For development (including the test, build, and lint tools):

```bash
python -m pip install -e ".[dev]"
```

> **PyPI note:** The normalized project name `python-dev-utils` is already registered to a different publisher. Confirm the exact PyPI project URL/name before using a `pip install`-from-PyPI command; do not assume this GitHub repository owns that existing PyPI listing.

## Quick start

### Hash a file

```python
from dev_utils import hash_file, sha256_file

# Backwards-compatible SHA-256 helper
sha256_digest = sha256_file("archive.zip")

# Choose another hashlib algorithm and a custom streaming chunk size
sha512_digest = hash_file(
    "archive.zip",
    algorithm="sha512",
    chunk_size=128 * 1024,
)
```

### Hash bytes

```python
from dev_utils import hash_bytes

digest = hash_bytes(b"hello", algorithm="sha256")
print(digest)
```

### Compare two files

```python
from dev_utils import files_are_equal

if files_are_equal("original.bin", "copy.bin"):
    print("Files contain identical bytes")
else:
    print("Files differ")
```

### Find duplicate files

```python
from dev_utils import find_duplicate_files

for duplicate_group in find_duplicate_files("./data"):
    print("Duplicate group:")
    for path in duplicate_group:
        print(f" - {path}")
```

The duplicate finder first groups candidates by file size, then compares content hashes. It is read-only: it does not delete or modify files. Symbolic links are skipped.

### Hash a directory tree

```python
from dev_utils import directory_hashes

manifest = directory_hashes(
    "./data",
    exclude_dirs=("__pycache__", ".git"),
)
for relative_path, digest in manifest.items():
    print(relative_path, digest)
```

This returns a deterministic mapping of relative POSIX paths to individual file digests. It does **not** calculate one combined directory digest. Symbolic links are not followed.

## API reference

| Function | Purpose |
|---|---|
| `hash_bytes(data, algorithm="sha256")` | Hash bytes and return a hexadecimal digest |
| `hash_file(path, algorithm="sha256", chunk_size=65536)` | Stream a file into a hash |
| `sha256_file(path)` | Backwards-compatible SHA-256 file helper |
| `files_are_equal(first, second, chunk_size=65536)` | Compare two files byte-for-byte |
| `find_duplicate_files(directory, recursive=True)` | Return groups of duplicate file paths |
| `directory_hashes(directory, algorithm="sha256", exclude_dirs=())` | Return a sorted per-file hash manifest |

File-system errors are generally propagated to the caller. Invalid hash algorithms and non-positive chunk sizes raise `ValueError`.

## Development

Run the test suite:

```bash
python -m unittest discover -s tests -v
```

Run Ruff:

```bash
ruff check .
```

Build the source and wheel distributions:

```bash
python -m build
```

GitHub Actions runs the test suite and lint checks on Python 3.10, 3.11, 3.12, and 3.13, and builds the package on Python 3.12.

## Contributing

Bug reports, focused feature proposals, documentation improvements, and tested pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history and unreleased changes.

## License

MIT. See [LICENSE](LICENSE).
