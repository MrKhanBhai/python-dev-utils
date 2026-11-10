# python-dev-utils

Small, dependency-free file utilities for Python developers.

**Python:** 3.10+ · **Runtime dependencies:** none · **License:** MIT

## Features

- Streaming file checksums with configurable hashlib algorithms.
- Hash bytes directly without creating a temporary file.
- Compare files byte-for-byte without loading them fully into memory.
- Find duplicate files by size and content hash (read-only; never deletes files).
- Produce deterministic per-file hashes for a directory tree.

## Installation

The package is not yet published to PyPI. Install from a local checkout:

```bash
git clone https://github.com/MrKhanBhai/python-dev-utils.git
cd python-dev-utils
python -m pip install .
```

For development tools:

```bash
python -m pip install -e ".[dev]"
```

## Usage

### Hash a file

```python
from dev_utils import hash_file, sha256_file

digest = sha256_file("archive.zip")
sha512 = hash_file("archive.zip", algorithm="sha512", chunk_size=128 * 1024)
```

### Hash bytes

```python
from dev_utils import hash_bytes

digest = hash_bytes(b"hello", algorithm="sha256")
```

### Compare two files

```python
from dev_utils import files_are_equal

if files_are_equal("original.bin", "copy.bin"):
    print("Files contain identical bytes")
```

### Find duplicate files

```python
from dev_utils import find_duplicate_files

for group in find_duplicate_files("./data"):
    print("Duplicate group:")
    for path in group:
        print(" -", path)
```

The finder groups candidates by size before hashing. It is read-only and does not remove or modify files. Symbolic links are skipped.

### Hash a directory tree

```python
from dev_utils import directory_hashes

manifest = directory_hashes("./data", exclude_dirs=("__pycache__", ".git"))
for relative_path, digest in manifest.items():
    print(relative_path, digest)
```

This returns a deterministic mapping of relative POSIX paths to individual file digests; it does not calculate one combined directory digest. Symbolic links are not followed.

## API reference

| Function | Purpose |
|---|---|
| `hash_bytes(data, algorithm="sha256")` | Hash bytes and return a hex digest |
| `hash_file(path, algorithm="sha256", chunk_size=65536)` | Stream a file into a hash |
| `sha256_file(path)` | Backwards-compatible SHA-256 helper |
| `files_are_equal(first, second, chunk_size=65536)` | Compare file contents |
| `find_duplicate_files(directory, recursive=True)` | Return groups of duplicate file paths |
| `directory_hashes(directory, algorithm="sha256", exclude_dirs=())` | Return a sorted per-file hash manifest |

File-system errors are generally propagated to the caller. Invalid hash algorithms and non-positive chunk sizes raise `ValueError`.

## Run tests

```bash
python -m unittest discover -s tests -v
```

Lint and formatting checks (after installing the development extra):

```bash
ruff check .
ruff format --check .
```

GitHub Actions tests Python 3.10, 3.11, 3.12, and 3.13.

## Contributing

Bug reports, focused feature proposals, documentation improvements, and tested pull requests are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Roadmap

See [CHANGELOG.md](CHANGELOG.md) for the current unreleased work and release history.

## License

MIT. See [LICENSE](LICENSE).
