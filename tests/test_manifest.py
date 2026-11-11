import json
import tempfile
import unittest
from pathlib import Path

from dev_utils.manifest import (
    build_manifest,
    load_manifest,
    verify_manifest,
    write_manifest,
)


class ManifestTests(unittest.TestCase):
    def test_build_manifest_is_deterministic(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "b.txt").write_text("beta", encoding="utf-8")
            (root / "a.txt").write_text("alpha", encoding="utf-8")
            manifest = build_manifest(root)
            self.assertEqual(list(manifest["files"]), ["a.txt", "b.txt"])
            self.assertEqual(manifest["manifest_version"], 1)

    def test_write_and_load_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "data"
            root.mkdir()
            (root / "hello.txt").write_text("hello", encoding="utf-8")
            manifest_path = Path(directory) / "manifest.json"
            written = write_manifest(root, manifest_path)
            self.assertEqual(load_manifest(manifest_path), written)
            self.assertTrue(
                manifest_path.read_text(encoding="utf-8").endswith("\n")
            )

    def test_excluded_directories_are_preserved_during_verification(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "data"
            (root / "cache").mkdir(parents=True)
            (root / "cache" / "generated.bin").write_bytes(b"cache")
            (root / "keep.txt").write_text("keep", encoding="utf-8")
            manifest = build_manifest(root, exclude_dirs=("cache",))
            result = verify_manifest(root, manifest)
            self.assertEqual(result, {
                "missing": [],
                "modified": [],
                "untracked": [],
            })
            self.assertEqual(manifest["exclude_dirs"], ["cache"])

    def test_write_load_and_verify_preserves_exclusions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "data"
            (root / ".cache").mkdir(parents=True)
            (root / ".cache" / "tmp").touch()
            manifest_path = Path(directory) / "manifest.json"
            write_manifest(root, manifest_path, exclude_dirs=(".cache",))
            loaded = load_manifest(manifest_path)
            self.assertEqual(loaded["exclude_dirs"], [".cache"])
            self.assertFalse(any(verify_manifest(root, loaded).values()))

    def test_legacy_manifest_without_exclusions_remains_supported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "data"
            root.mkdir()
            (root / "file.txt").write_text("data", encoding="utf-8")
            manifest = build_manifest(root)
            manifest.pop("exclude_dirs")
            self.assertFalse(any(verify_manifest(root, manifest).values()))

    def test_verify_clean_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "data"
            root.mkdir()
            (root / "hello.txt").write_text("hello", encoding="utf-8")
            expected = {"missing": [], "modified": [], "untracked": []}
            self.assertEqual(verify_manifest(root, build_manifest(root)), expected)

    def test_verify_reports_all_change_types(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "data"
            root.mkdir()
            (root / "modified.txt").write_text("before", encoding="utf-8")
            (root / "missing.txt").write_text("remove", encoding="utf-8")
            manifest = build_manifest(root)
            (root / "modified.txt").write_text("after", encoding="utf-8")
            (root / "missing.txt").unlink()
            (root / "new.txt").write_text("new", encoding="utf-8")
            expected = {
                "missing": ["missing.txt"],
                "modified": ["modified.txt"],
                "untracked": ["new.txt"],
            }
            self.assertEqual(verify_manifest(root, manifest), expected)

    def test_can_ignore_untracked_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "data"
            root.mkdir()
            manifest = build_manifest(root)
            (root / "extra").touch()
            result = verify_manifest(root, manifest, include_untracked=False)
            self.assertEqual(result["untracked"], [])

    def test_rejects_unsupported_version(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            data = {
                "manifest_version": 99,
                "algorithm": "sha256",
                "files": {},
            }
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unsupported manifest version"):
                load_manifest(path)

    def test_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            data = {
                "manifest_version": 1,
                "algorithm": "sha256",
                "files": {"../outside": "0" * 64},
            }
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unsafe manifest path"):
                load_manifest(path)

    def test_rejects_invalid_digest(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            data = {
                "manifest_version": 1,
                "algorithm": "sha256",
                "files": {"file.txt": "not-a-digest"},
            }
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_manifest(path)

    def test_rejects_invalid_excluded_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            data = {
                "manifest_version": 1,
                "algorithm": "sha256",
                "exclude_dirs": ["cache", 3],
                "files": {},
            }
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "exclude_dirs"):
                load_manifest(path)


if __name__ == "__main__":
    unittest.main()
