import hashlib
import tempfile
import unittest
from pathlib import Path

from dev_utils.directory_hash import directory_hashes


class DirectoryHashTests(unittest.TestCase):
    def test_hashes_files_with_relative_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.txt").write_bytes(b"alpha")
            nested = root / "nested"
            nested.mkdir()
            (nested / "b.txt").write_bytes(b"beta")
            result = directory_hashes(root)
            self.assertEqual(list(result), ["a.txt", "nested/b.txt"])
            self.assertEqual(result["a.txt"], hashlib.sha256(b"alpha").hexdigest())

    def test_excludes_named_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            excluded = root / "build"
            excluded.mkdir()
            (excluded / "artifact").write_text("x", encoding="utf-8")
            (root / "keep").write_text("y", encoding="utf-8")
            actual = list(directory_hashes(root, exclude_dirs=("build",)))
            self.assertEqual(actual, ["keep"])

    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(directory_hashes(directory), {})

    def test_invalid_algorithm_is_rejected_for_empty_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "unsupported hash algorithm"):
                directory_hashes(directory, algorithm="not-real")

    def test_exclude_dirs_must_be_names(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(TypeError):
                directory_hashes(directory, exclude_dirs="build")

    def test_symlink_files_are_skipped(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target.txt"
            target.write_text("content", encoding="utf-8")
            link = root / "link.txt"
            try:
                link.symlink_to(target)
            except (NotImplementedError, OSError):
                self.skipTest("symlinks are not available on this platform")
            self.assertEqual(list(directory_hashes(root)), ["target.txt"])

    def test_non_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "file"
            path.touch()
            with self.assertRaises(NotADirectoryError):
                directory_hashes(path)

    def test_unsupported_algorithm(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "file").write_text("x", encoding="utf-8")
            with self.assertRaises(ValueError):
                directory_hashes(directory, algorithm="not-real")


if __name__ == "__main__":
    unittest.main()
