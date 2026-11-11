# Changelog

## 0.3.1

- Rename the PyPI distribution to `mrkhanbhai-python-dev-utils` because `python-dev-utils` is registered to another publisher.
- Add a GitHub Actions Trusted Publishing workflow using PyPI OIDC; no long-lived PyPI API token is stored in GitHub.

Notable changes to python-dev-utils are documented here.

## 0.3.0

- Add the `dev-utils` CLI for hashing, file comparison, duplicate discovery, and directory manifest operations.
- Add versioned JSON directory manifests with loading, validation, and verification reports for missing, modified, and untracked files.
- Preserve excluded directory settings when verifying manifests and improve input validation for hash algorithms and directory exclusions.
- Add PEP 561 typing metadata and expand CI across Python 3.10–3.13 on Ubuntu, Windows, and macOS.
- Expand regression coverage and documentation for the new APIs and CLI.

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
