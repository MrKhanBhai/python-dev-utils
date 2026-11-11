"""Command-line interface for python-dev-utils."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .checksum import hash_file
from .duplicate_finder import find_duplicate_files
from .file_compare import files_are_equal
from .manifest import verify_manifest, write_manifest


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dev-utils",
        description="Small file utilities for developers.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    hashing = commands.add_parser("hash", help="Hash a file")
    hashing.add_argument("file", type=Path)
    hashing.add_argument("--algorithm", default="sha256")
    hashing.add_argument("--chunk-size", type=int, default=64 * 1024)

    compare = commands.add_parser(
        "compare", help="Compare two files byte-for-byte"
    )
    compare.add_argument("first", type=Path)
    compare.add_argument("second", type=Path)

    duplicates = commands.add_parser(
        "duplicates", help="Find duplicate files without modifying them"
    )
    duplicates.add_argument("directory", type=Path)
    duplicates.add_argument("--non-recursive", action="store_true")

    create = commands.add_parser(
        "manifest", help="Create a JSON directory manifest"
    )
    create.add_argument("directory", type=Path)
    create.add_argument("output", type=Path)
    create.add_argument("--algorithm", default="sha256")
    create.add_argument("--exclude-dir", action="append", default=[])

    verify = commands.add_parser(
        "verify", help="Verify a directory against a JSON manifest"
    )
    verify.add_argument("directory", type=Path)
    verify.add_argument("manifest", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    args = _parser().parse_args(argv)

    if args.command == "hash":
        print(hash_file(args.file, args.algorithm, args.chunk_size))
        return 0

    if args.command == "compare":
        equal = files_are_equal(args.first, args.second)
        print("identical" if equal else "different")
        return 0 if equal else 1

    if args.command == "duplicates":
        groups = find_duplicate_files(
            args.directory, recursive=not args.non_recursive
        )
        print(
            json.dumps(
                [[str(path) for path in group] for group in groups],
                indent=2,
            )
        )
        return 0

    if args.command == "manifest":
        data = write_manifest(
            args.directory,
            args.output,
            args.algorithm,
            tuple(args.exclude_dir),
        )
        print(f"Manifest written: {args.output} ({len(data['files'])} files)")
        return 0

    if args.command == "verify":
        result = verify_manifest(args.directory, args.manifest)
        print(json.dumps(result, indent=2))
        return 0 if not any(result.values()) else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
