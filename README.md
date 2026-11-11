# python-dev-utils

Small, dependency-free file utilities for Python developers.

[![Python versions](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Python:** 3.10+ · **Runtime dependencies:** none · **Type hints:** PEP 561 · **License:** MIT

## Features

- Stream file contents into a hash using any algorithm supported by `hashlib`.
- Hash in-memory `bytes` without creating a temporary file.
- Compare two files byte-for-byte without reading either file fully into memory.
- Find duplicate files by size and content hash (read-only; never deletes files).
- Generate, save, load, and verify deterministic JSON manifests for directory trees.
- Use the same tools from Python or the `dev-utils` command-line interface.

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

For development (including test, build, and lint tools), run this from the repository root:

```bash
python -m pip install -e ".[dev]"
```

> **PyPI note:** The normalized project name `python-dev-utils` is already registered to a different publisher. Confirm the exact PyPI project URL/name before using a PyPI install command; do not assume this repository owns that listing.

## Quick start

### Hash a file or bytes

```python
from dev_utils import hash_bytes, hash_file, sha256_file

sha256_digest = sha256_file("archive.zip")  # Backwards-compatible helper
sha512_digest = hash_file("archive.zip", algorithm="sha512", chunk_size=128 * 1024)
memory_digest = hash_bytes(b"hello", algorithm="sha256")
```

### Compare files and find duplicates

```python
from dev_utils import files_are_equal, find_duplicate_files

if files_are_equal("original.bin", "copy.bin"):
    print("Files contain identical bytes")

for group in find_duplicate_files("./data"):
    print([str(path) for path in group])
```

The duplicate finder groups candidates by size before hashing. It is read-only and skips symbolic links.

### Create and verify a directory manifest

```python
from dev_utils import write_manifest, verify_manifest

# Store the manifest outside the directory being scanned.
write_manifest("./data", "../data-manifest.json", exclude_dirs=(".git", "__pycache__"))

result = verify_manifest("./data", "../data-manifest.json")
if any(result.values()):
    print("Directory differs from the manifest:", result)
else:
    print("Directory matches the manifest")
```

A verification result contains sorted `missing`, `modified`, and `untracked` relative paths. Verification never changes files. The manifest stores per-file digests; it is not a single combined directory digest. Symbolic links are not followed.

## Command-line interface

Installing the package creates the `dev-utils` command:

```bash
# Hash a file
dev-utils hash archive.zip --algorithm sha256

# Compare two files (exit 0 if identical, 1 if different)
dev-utils compare original.bin copy.bin

# List duplicate groups
dev-utils duplicates ./data
dev-utils duplicates ./data --non-recursive

# Create a JSON manifest; keep output outside the scanned directory
dev-utils manifest ./data ../data-manifest.json --exclude-dir .git

# Verify against a saved manifest (exit 0 if clean, 1 if differences found)
dev-utils verify ./data ../data-manifest.json
```

## API reference

| Function | Purpose |
|---|---|
| `hash_bytes(data, algorithm="sha256")` | Hash bytes and return a hexadecimal digest |
| `hash_file(file_path, algorithm="sha256", chunk_size=65536)` | Stream a file into a hash |
| `sha256_file(path)` | Backwards-compatible SHA-256 file helper |
| `files_are_equal(first, second, chunk_size=65536)` | Compare two files byte-for-byte |
| `find_duplicate_files(directory, recursive=True)` | Return groups of duplicate file paths |
| `directory_hashes(directory, algorithm="sha256", exclude_dirs=())` | Return a sorted per-file hash mapping |
| `build_manifest(directory, algorithm="sha256", exclude_dirs=())` | Build versioned manifest data |
| `write_manifest(directory, manifest_path, ...)` | Write a JSON manifest |
| `load_manifest(manifest_path)` | Load and validate a JSON manifest |
| `verify_manifest(directory, manifest, include_untracked=True)` | Report missing, modified, and untracked files |

File-system errors are generally propagated to the caller. Unsupported algorithms and non-positive chunk sizes raise `ValueError`.

## Development

```bash
python -m unittest discover -s tests -v
ruff check .
python -m build
```

GitHub Actions runs tests, lint checks, coverage reporting, and a CLI smoke test on Python 3.10–3.13 across Ubuntu, Windows, and macOS. It builds the package on Ubuntu with Python 3.12.

## Contributing

Bug reports, focused feature proposals, documentation improvements, and tested pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history and unreleased changes.

## License

MIT. See [LICENSE](LICENSE).
