# python-dev-utils

Small, dependency-free Python utilities for everyday developer workflows.

## Current utility

### SHA-256 file checksums

Calculate a SHA-256 digest without loading the entire file into memory:

```python
from dev_utils.checksum import sha256_file

digest = sha256_file("path/to/file.bin")
print(digest)
```

The function reads files in 64 KiB chunks and returns the digest as a lowercase hexadecimal string. It supports text and binary files. Standard file-opening errors (such as `FileNotFoundError` and `PermissionError`) are allowed to propagate to the caller.

## Run the tests

Requires Python 3.10 or newer. No third-party packages are needed.

```bash
python -m unittest discover -s tests -v
```

## Project layout

```text
dev_utils/
  __init__.py
  checksum.py
tests/
  test_checksum.py
```

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE).

Contributions that fix bugs, improve documentation, or add focused, tested utilities are welcome. Please include tests for behavior changes.
