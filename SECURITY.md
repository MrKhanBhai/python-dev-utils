# Security Policy

## Reporting a vulnerability

Please do not publish details of an exploitable security issue in a public issue or pull request.

If GitHub private vulnerability reporting is enabled for this repository, use the repository's **Security** tab and choose **Report a vulnerability**. Otherwise, contact the maintainer through the GitHub profile and ask for a private channel to share the report.

Include the affected version or commit, the impact, and clear reproduction steps. Please allow reasonable time for investigation and a fix before public disclosure.

## Scope

The project provides local file hashing, comparison, duplicate discovery, and directory-manifest utilities. These operations are intended to be read-only except for explicitly requested manifest output. Reports involving unexpected file modification, path handling, symlink behavior, or unsafe manifest input are especially useful.
