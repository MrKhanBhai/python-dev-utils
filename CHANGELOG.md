# Changelog

Notable changes to python-dev-utils are documented here.

## 0.2.0

- Add generic streaming file hashing and bytes hashing.
- Preserve the existing `sha256_file` helper for backwards compatibility.
- Add chunked byte-for-byte file comparison.
- Add read-only duplicate file discovery, grouping candidates by size and content hash.
- Add deterministic per-file directory hash manifests.
- Expand unit tests and CI coverage to Python 3.10–3.13.
- Add Ruff linting, package metadata, and contributor documentation.

## Unreleased

- Harden hash algorithm and directory input validation; reject variable-length SHAKE algorithms with a clear error.
- Preserve excluded directory names in manifests so verification uses the same scan scope.
- Add versioned JSON directory manifests with validation and verification reports.
- Add the `dev-utils` CLI for hashing, comparison, duplicate discovery, and manifests.
- Add PEP 561 typing metadata and expand cross-platform CI to Ubuntu, Windows, and macOS.
