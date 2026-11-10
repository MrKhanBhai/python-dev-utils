import tempfile
import unittest
from pathlib import Path
from dev_utils.file_compare import files_are_equal

class FileCompareTests(unittest.TestCase):
    def test_identical_files(self):
        with tempfile.TemporaryDirectory() as directory:
            a, b = Path(directory) / "a", Path(directory) / "b"
            a.write_bytes(b"same content")
            b.write_bytes(b"same content")
            self.assertTrue(files_are_equal(a, b, chunk_size=3))

    def test_different_same_size(self):
        with tempfile.TemporaryDirectory() as directory:
            a, b = Path(directory) / "a", Path(directory) / "b"
            a.write_bytes(b"abcd")
            b.write_bytes(b"abce")
            self.assertFalse(files_are_equal(a, b))

    def test_different_sizes(self):
        with tempfile.TemporaryDirectory() as directory:
            a, b = Path(directory) / "a", Path(directory) / "b"
            a.write_bytes(b"a")
            b.write_bytes(b"longer")
            self.assertFalse(files_are_equal(a, b))

    def test_empty_files(self):
        with tempfile.TemporaryDirectory() as directory:
            a, b = Path(directory) / "a", Path(directory) / "b"
            a.touch()
            b.touch()
            self.assertTrue(files_are_equal(a, b))

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                files_are_equal(Path(directory) / "missing", Path(directory) / "other")

    def test_invalid_chunk_size(self):
        with tempfile.TemporaryDirectory() as directory:
            a, b = Path(directory) / "a", Path(directory) / "b"
            a.touch()
            b.touch()
            with self.assertRaises(ValueError):
                files_are_equal(a, b, chunk_size=0)

if __name__ == "__main__":
    unittest.main()
