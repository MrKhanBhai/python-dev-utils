import hashlib
import tempfile
import unittest
from pathlib import Path

from dev_utils.checksum import sha256_file


class ChecksumTests(unittest.TestCase):
    def test_sha256_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_bytes(b"hello world")

            expected = hashlib.sha256(b"hello world").hexdigest()
            self.assertEqual(sha256_file(str(path)), expected)

    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.bin"
            path.write_bytes(b"")

            self.assertEqual(sha256_file(str(path)), hashlib.sha256(b"").hexdigest())

    def test_binary_file(self):
        content = bytes(range(256))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "binary.bin"
            path.write_bytes(content)

            self.assertEqual(sha256_file(str(path)), hashlib.sha256(content).hexdigest())

    def test_missing_file_raises_file_not_found_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing.txt"

            with self.assertRaises(FileNotFoundError):
                sha256_file(str(path))


if __name__ == "__main__":
    unittest.main()
